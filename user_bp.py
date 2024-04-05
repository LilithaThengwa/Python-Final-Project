from flask import flash
from flask import Blueprint, render_template, request, redirect, url_for, session
from app import db, Customer, RegistrationForm, LoginForm, Policies, ApplyPolicyForm, PolicyType, Claims, FileClaimForm

user_bp = Blueprint("user_bp", __name__)

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
        # new_customer = Customer(Username=form.username.data, Password=form.password.data)
        new_customer = Customer()
        for key, value in request.form.items():
            if hasattr(new_customer, key):
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
        customer = Customer.query.filter_by(Username=form.username.data, Password=form.password.data).first()
        if customer:
            session["CustomerID"] = customer.CustomerID
            return redirect(url_for("user_bp.customer_dashboard", customer=customer, policies=customer.policies))
                           
  
    return render_template("login.html", form=form)

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

@user_bp.route('/get_quote', methods=['POST'])
def get_quote():
    cover_type = request.form['cover_type']
    criminal_record = request.form.get('criminal_record') 
    tried = request.form.get('tried') 
    arrested = request.form.get('arrested') 
    none = request.form.get('none')
    government_official = request.form['government_official']
    age = int(request.form['age'])
    occupation = request.form['occupation']

    premuim = calculate_premium(cover_type, criminal_record, tried, arrested, none, government_official, age, occupation)

    return render_template("quote.html", premuim=premuim)

def calculate_premium(cover_type, criminal_record, tried, arrested, none, government_official, age, occupation):
    cover_amount = {
        "Basic Coverage": 40_000,
        "Standard Coverage": 80_000,
        "Comprehensive Coverage": 160_000,
        "Customized Coverage": 60_000
    }.get(cover_type, 0)

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