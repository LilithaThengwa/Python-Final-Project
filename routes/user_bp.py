from extensions import db
from flask import flash
from flask import Blueprint, render_template, request, redirect, url_for, session
from wtforms.validators import InputRequired, Email, Length
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, DecimalField, DateField, HiddenField
from wtforms.validators import InputRequired, Length, ValidationError, DataRequired
from datetime import date
from flask_wtf import FlaskForm
from models.customer import Customer
from models.policy import Policies
from models.claim import Claims
from models.policy_type import PolicyType
from models.admin import Admin
from flask_login import login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

user_bp = Blueprint("user_bp", __name__)

class RegistrationForm(FlaskForm): 
    FirstName = StringField("First Name", validators=[InputRequired(), Length(min=2)])
    LastName = StringField("Last Name", validators=[InputRequired(), Length(min=2)])
    PhoneNumber = StringField("Phone Number", validators=[InputRequired(), Length(min=2)])
    Username = StringField("Username", validators=[InputRequired(), Length(min=2)])
    Email = StringField("Email", validators=[InputRequired(), Length(min=2)])
    Password = PasswordField("Password", validators=[InputRequired(), Length(min=2)])
    submit = SubmitField("Sign Up")

    def validate_username(self, field):
        if Customer.query.filter_by(Username=field.data).first():
           raise ValidationError("Username taken.")

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=2)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=2, max=12)])
    submit = SubmitField("Log in")

    def validate_username(self, field):
        if not Customer.query.filter_by(Username=field.data).first():
            raise ValidationError("Invalid credentials")
        
    def validate_password(self, field):
        customer_from_db =  Customer.query.filter_by(Username=self.username.data).first()
        if customer_from_db:
          form_password = field.data
          user_db_data = customer_from_db.to_dict()
          if not check_password_hash(user_db_data["Password"], form_password):
            raise ValidationError("Invalid credentials")
        # if user_from_db:
        #   if not Customer.query.filter_by(Username=self.username.data, Password=field.data).first():
        #     raise ValidationError("Invalid credentials")

class ApplyPolicyForm(FlaskForm):
    policy_type = SelectField("Policy Type", validators=[DataRequired()])
    item_insured = StringField("Item Insured", validators=[DataRequired()])
    insured_value = DecimalField("Insured Value", validators=[DataRequired()])
    monthly_premium = DecimalField("Monthly Premium", validators=[DataRequired()])
    date_applied = DateField("Date", validators=[DataRequired()], default=date.today, render_kw={"readonly": True})
    CustomerID = HiddenField("Customer ID")

class FileClaimForm(FlaskForm):
    Policy = SelectField("Select a Policy from which to claim", validators=[DataRequired()])
    date_of_event = DateField("Date of Loss", validators=[DataRequired()])
    Date_Filed = DateField("Current Date", validators=[DataRequired()], default=date.today, render_kw={"readonly": True})
    Description = TextAreaField("Description", validators=[DataRequired()])
    Amount = DecimalField("Amount claiming for", validators=[DataRequired()])
    CustomerID = HiddenField("Customer ID")
    submit = SubmitField("Submit")

@user_bp.route("/dashboard")
def customer_dashboard():
    customer_id = session.get("CustomerID")
    if not customer_id:
        return redirect(url_for("user_bp.login"))

    customer = Customer.query.get(customer_id)
    if not customer:
        return "Customer not found", 404

    # customer_policies = Policies.query.filter_by(CustomerID=customer_id).all()
    # customer_claims = Claims.query.filter_by(CustomerID=customer_id).all()
    print(customer.policies)

    return render_template("customerdashboard.html", customer=customer, policies=customer.policies, claims=customer.claims)
                           

@user_bp.route("/register", methods=["GET","POST"])
def register():
    #GET and POST
    form = RegistrationForm()
    
    #only when POST
    if form.validate_on_submit():
        # if User.query.filter_by(username=form.username.data).first():
        #     return render_template("register.html", form=form)
        password_hash = generate_password_hash(form.Password.data)
        new_customer = Customer()
        for key, value in request.form.items():
            if hasattr(new_customer, key):
                if key == "Password":
                 setattr(new_customer, key, password_hash)
                else:
                 setattr(new_customer, key, value)

        try:
          db.session.add(new_customer)
          db.session.commit()
          return render_template("customerdashboard.html", customer=new_customer)
        except Exception as e:
            db.session.rollback()
            return f"<h2>error{str(e)}</h2>", 500

    # only GET
    return render_template("register.html", form=form)

@user_bp.route("/login", methods=["GET","POST"])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        customer = Customer.query.filter_by(Username=form.username.data).first()
        print("start")
        print(customer.FirstName)
        if customer:
            login_user(customer)
            flash('You were successfully logged in')
            session["CustomerID"] = customer.CustomerID
            if customer.role == "user":
                    return redirect(url_for("user_bp.customer_dashboard", customer=customer, policies=customer.policies))
            elif customer.role == "admin":
               
                return redirect(url_for("admin_bp.admin_dashboard"))
                           
    return render_template("login.html", form=form)

@user_bp.route("/logout", methods=["GET", "POST"])
def logout():
    logout_user()
    return redirect(url_for("user_bp.login"))

@user_bp.route("/registerforpolicy", methods=["POST"])  
def show_register_for_policy():
    form = ApplyPolicyForm()
    form.policy_type.choices = [(policy_type.PolicyTypeID, policy_type.name) for policy_type in PolicyType.query.all()]
    customerID = request.form.get("CustomerID")
    customer = Customer.query.get(customerID) 
    return render_template("register-for-policy.html", form=form, customer=customer, policies=customer.policies)

@user_bp.route("/registerforpolicy/<CustomerID>", methods=["GET","POST"])  
def register_for_policy(CustomerID):
    form = ApplyPolicyForm()
    form.policy_type.choices = [(policy_type.PolicyTypeID, policy_type.name) for policy_type in PolicyType.query.all()]
    customer = Customer.query.get(CustomerID) 
    if form.validate_on_submit():
        new_policy = Policies()
        form.CustomerID.data = CustomerID  # Assign CustomerID to form correctly
        new_policy.CustomerID = CustomerID
        policy_type_id = form.policy_type.data  
        policy_type = PolicyType.query.get(policy_type_id)
        new_policy.policy_type = policy_type
        new_policy.ItemInsured = form.item_insured.data
        new_policy.InsuredValue = form.insured_value.data
        new_policy.MonthlyPremium = form.monthly_premium.data
        new_policy.DateTakenOut = form.date_applied.data
        new_policy.DateActive = form.date_applied.data #change later
        
        try:
          db.session.add(new_policy)
          db.session.commit()
          return render_template("customerdashboard.html", customer=customer, policies=Policies.query.filter_by(CustomerID=customer.CustomerID).distinct())
        except Exception as e:
            db.session.rollback()
            return f"<h2>error{str(e)}</h2>", 500
    return render_template("register-for-policy.html", form=form, customer=customer, policies=Policies.query.filter_by(CustomerID=customer.CustomerID).distinct(), 
                           claims=Claims.query.filter_by(CustomerID=customer.CustomerID).distinct())

@user_bp.route("/fileclaim", methods=["POST"])  
def show_file_claim():
    form =FileClaimForm()
    form.Policy.choices = [(policy.PolicyID, policy.ItemInsured) for policy in Policies.query.all()]
    customerID = request.form.get("CustomerID")
    customer = Customer.query.get(customerID) 
    # customer_policies = Policies.query.filter_by(CustomerID=customerID)
    return render_template("file-claim.html", form=form, customer=customer, policies=customer.policies)

@user_bp.route("/fileclaim/<CustomerID>", methods=["GET", "POST"])
def file_claim(CustomerID):
    form = FileClaimForm()
    customer_policies = Policies.query.filter_by(CustomerID=CustomerID).all() 
    form.Policy.choices = [(policy.PolicyID, policy.ItemInsured) for policy in customer_policies]
    customer = Customer.query.get(CustomerID)
    if form.validate_on_submit():
        print("submit success")
        new_claim = Claims(
            CustomerID=CustomerID,
            PolicyID=form.Policy.data,
            Description=form.Description.data,
            Amount=form.Amount.data,
            DateFiled=form.Date_Filed.data
        )
        try:
            db.session.add(new_claim)
            db.session.commit()
            return redirect(url_for("user_bp.customer_dashboard", customer=customer, policies=customer.policies))
        except Exception as e:
            db.session.rollback()
            return f"<h2>Error: {str(e)}</h2>", 500
    else:
        print(form.errors)
    print("no submit")
    return render_template("file-claim.html", form=form, customer=customer, policies=customer.policies)

@user_bp.route("/get_quote", methods=["POST"])
def get_quote():
    cover_type = request.form["cover_type"]
    criminal_record = request.form.get("criminal_record")
    tried = request.form.get("tried")
    arrested = request.form.get("arrested")
    none = request.form.get("none")
    government_official = request.form["government_official"]
    age = int(request.form["age"])
    occupation = request.form["occupation"]

    premuim = calculate_premium(cover_type, criminal_record, tried, arrested, none, government_official, age, occupation)

    return render_template("quote.html", premuim=premuim)

def calculate_premium(cover_type, criminal_record, tried, arrested, none, government_official, age, occupation):
    cover_amount_limits = {
        "Basic Coverage": 40_000,
        "Standard Coverage": 80_000,
        "Comprehensive Coverage": 160_000,
        "Customized Coverage": 60_000
    }.get(cover_type, 0)
    
    print(cover_amount_limits)
    premium_rates = {
        "Basic Coverage": 900,
        "Standard Coverage": 1900,
        "Comprehensive Coverage": 3000,
        "Customized Coverage": 1250
    }

    premium = 5000

    premium = premium_rates.get(cover_type, 0)

    if criminal_record:
        premium += 1000
    if tried:
        premium += 700
    if arrested:
        premium += 500
    if government_official == "Yes":
        return "Unfortunately we cannot provide you with cover."

    if age < 30:
        premium += 100  
    elif age >= 60:
        premium -= 200 

    return premium