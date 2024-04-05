from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from dotenv import load_dotenv
import os
import uuid
from flask_wtf import FlaskForm
from sqlalchemy import select
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, Email, Length
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, DecimalField, DateField, HiddenField, BooleanField, IntegerField
from wtforms.validators import InputRequired, Length, ValidationError, Email, DataRequired
from datetime import date

app = Flask(__name__)

load_dotenv()
connection_string = os.environ.get("AZURE_DATABASE_URL")

x = 3

 
app.config["SECRET_KEY"] = os.environ.get("FORM_SECRET_KEY")
print(os.environ.get("FORM_SECRET_KEY"))
app.config["SQLALCHEMY_DATABASE_URI"] = connection_string
db = SQLAlchemy(app)

class Customer(db.Model):
     __tablename__ = "Customer"
     CustomerID = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
     FirstName = db.Column(db.String(50), nullable=False)
     LastName = db.Column(db.String(50), nullable=False)
     Username = db.Column(db.String(50), nullable=False, unique=True)
     PhoneNumber = db.Column(db.String(50), nullable=False)
     Email = db.Column(db.String(50), nullable=False)
     Password = db.Column(db.String(100), nullable=False)

     def to_dict(self):
        return {
            "CustomerID" : self.CustomerID,
            "FirstName": self.FirstName,
            "LastName": self.LastName,
            "Username": self.Username,
            "Password": self.Password,
            "PhoneNumber": self.PhoneNumber,
            "Email": self.Email,
            "Password": self.Password,    
        }
     
     policies = db.relationship("Policies", back_populates="customer")
     claims = db.relationship("Claims", back_populates="customer")
     
class PolicyType(db.Model):
    __tablename__ = "PolicyType"

    PolicyTypeID = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    short_description = db.Column(db.String(100), nullable=False)
    img = db.Column(db.String(255), nullable=False)
    alt = db.Column(db.String(50), nullable=False)

    def to_dict(self):
        return {
            "PolicyTypeID": self.PolicyTypeID,
            "name": self.name,
            "description": self.description,
            "short_description": self.short_description,
            "img": self.img,
            "alt": self.alt
        }
    
    policies = db.relationship("Policies", back_populates="policy_type")
    
class Policies(db.Model):
    __tablename__ = "Policies"
    
    PolicyID = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    CustomerID = db.Column(db.String(50), db.ForeignKey('Customer.CustomerID'))
    PolicyTypeID = db.Column(db.String(50), db.ForeignKey('PolicyType.PolicyTypeID'))
    ItemInsured = db.Column(db.String(255), nullable=False)
    InsuredValue = db.Column(db.DECIMAL(18, 2), nullable=False)
    MonthlyPremium = db.Column(db.DECIMAL(18, 2), nullable=False)
    DateTakenOut = db.Column(db.Date, nullable=False)
    DateActive = db.Column(db.Date, nullable=False)
    Status = db.Column(db.String(20), default='Active')
    
    # Define the relationship with Customer and PolicyType tables
    customer = db.relationship("Customer", back_populates="policies", foreign_keys=[CustomerID])
    policy_type = db.relationship("PolicyType", back_populates="policies")
    claims = db.relationship("Claims", back_populates="policy")

class LegalInsuranceEstimateForm(FlaskForm):
    cover_amount = IntegerField("Cover Amount Required", validators=[DataRequired()])
    cover_type = SelectField("Level of Cover Required", choices=[
        ("", "Select Cover Level"),
        ("Basic Coverage", "Basic Coverage"),
        ("Standard Coverage", "Standard Coverage"),
        ("Comprehensive Coverage", "Comprehensive Coverage"),
        ("Customized Coverage", "Customized Coverage")
    ], validators=[DataRequired()])
    criminal_record = BooleanField("Criminal record")
    tried = BooleanField("Have been tried and found not guilty")
    arrested = BooleanField("Have been arrested or been the subject of criminal investigation")
    none = BooleanField("Never been arrested or been the subject of criminal investigation")
    government_official = SelectField("Are you, or any of your close relatives high ranking government officials?", choices=[
        ("", "Select"),
        ("Yes", "Yes"),
        ("No", "No")
    ], validators=[DataRequired()])
    age = IntegerField("Age", validators=[DataRequired()])
    occupation = StringField("Occupation", validators=[DataRequired()])
    # marital_status = SelectField("Marital status", choices=[
    #     ("", "Select Marital status"),
    #     ("Never Married", "Never Married"),
    #     ("Community of property", "Married in Community of Property"),
    #     ("Out of community", "Married out of Community of Property"),
    #     ("Divorced", Divorced")
    # ], validators=[DataRequired()])
    submit = SubmitField("Get Estimate")
class Claims(db.Model):
    __tablename__ = "Claims"

    ClaimID = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    PolicyID = db.Column(db.String(50), db.ForeignKey('Policies.PolicyID'))
    CustomerID = db.Column(db.String(50), db.ForeignKey('Customer.CustomerID'))
    DateFiled = db.Column(db.Date, nullable=False)
    Description = db.Column(db.String(255), nullable=False)
    Amount = db.Column(db.DECIMAL(18, 2), nullable=False)
    Status = db.Column(db.String(20), default='Pending')

    # Define the relationship with Policies and Customer tables
    policy = db.relationship("Policies", back_populates="claims")
    customer = db.relationship("Customer", back_populates="claims")

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
        user_from_db =  Customer.query.filter_by(Username=self.username.data).first()
        # if user_from_db:
        # form_password = field.data
        # user_db_data = user_from_db.to_dict()
        # if user_db_data["password"] != form_password:
        #     raise ValidationError("Invalid credentials")
        if user_from_db:
          if not Customer.query.filter_by(Username=self.username.data, Password=field.data).first():
            raise ValidationError("Invalid credentials")
          
class UpdateCustomerForm(FlaskForm):
    FirstName = StringField("First Name", validators=[InputRequired(), Length(max=50)])
    LastName = StringField("Last Name", validators=[InputRequired(), Length(max=50)])
    Email = StringField("Email", validators=[InputRequired(), Email(), Length(max=50)])
    PhoneNumber = StringField("Phone Number", validators=[InputRequired(), Length(max=20)])
    submit = SubmitField("Update")

class UpdatePolicyTypeForm(FlaskForm):
    name = StringField("Name", validators=[InputRequired(), Length(max=50)])
    description = TextAreaField("Description", validators=[InputRequired(), Length(max=255)])
    short_description = TextAreaField("Short Description", validators=[InputRequired(), Length(max=255)])
    img = StringField("Image URL", validators=[InputRequired(), Length(max=255)])
    alt = StringField("Alt Text", validators=[InputRequired(), Length(max=50)])
    submit = SubmitField("Update")

# =============================================================================================================================

@app.context_processor
def inject_items():
    items = [policy for policy in PolicyType.query.all()] 
    return dict(nav_dopdown_items=items)

@app.route("/")
def home():
    return render_template("home.html", policyTypes=PolicyType.query.all())

# =============================================================================================================================
# =============================================================================================================================

@app.route("/policy/<id>")
def policy(id):
    form = LegalInsuranceEstimateForm()
    # perform calculations
    policy_type = PolicyType.query.get(id)
    if policy:
        return render_template("policy.html", policy=policy_type, form=form)
    else:
        return f"Policy not found for ID: {id}", 404 
    
@app.route("/quote")
def quote():
    return render_template("quote.html")
    
if __name__ == "__main__":
    app.run(debug = True)

from about_bp import about_bp
from user_bp import user_bp
from admin_bp import admin_bp

app.register_blueprint(about_bp, url_prefix="/about")
app.register_blueprint(user_bp, url_prefix="/user")
app.register_blueprint(admin_bp, url_prefix="/admin")