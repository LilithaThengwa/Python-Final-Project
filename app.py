from flask import Flask, render_template, session
from dotenv import load_dotenv
import os
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, DecimalField, DateField, HiddenField, BooleanField, IntegerField
from wtforms.validators import InputRequired, Length, ValidationError, Email, DataRequired
from datetime import date
from extensions import db
from models.policy_type import PolicyType
from models.customer import Customer
from flask_login import LoginManager
login_manager = LoginManager()

app = Flask(__name__)

load_dotenv()
connection_string = os.environ.get("LOCAL_DATABASE_URL")

app.config["SECRET_KEY"] = os.environ.get("FORM_SECRET_KEY")
print(os.environ.get("FORM_SECRET_KEY"))
app.config["SQLALCHEMY_DATABASE_URI"] = connection_string
# db = SQLAlchemy(app)
db.init_app(app)
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return Customer.query.get(user_id)

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
    marital_status = SelectField("Marital status", choices=[
        ("", "Select Marital status"),
        ("Never Married", "Never Married"),
        ("Community of property", "Married in Community of Property"),
        ("Out of community", "Married out of Community of Property"),
        ("Divorced", "Divorced")
    ], validators=[DataRequired()])
    submit = SubmitField("Get Estimate")

# =============================================================================================================================

@app.context_processor
def inject_items():
    items = [policy for policy in PolicyType.query.all()] 
    return dict(nav_dopdown_items=items)

@app.context_processor
def inject_user_role():
    user_role = session.get("user_role")
    return dict(user_role=user_role)

@app.route("/")
def home():
    return render_template("home.html", policyTypes=PolicyType.query.all())

# =============================================================================================================================
# =============================================================================================================================

@app.route("/policy/<id>")
def policy(id):
    form = LegalInsuranceEstimateForm()
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

from routes.about_bp import about_bp
from routes.user_bp import user_bp
from routes.admin_bp import admin_bp
from routes.main_bp import main_bp

app.register_blueprint(about_bp, url_prefix="/about")
app.register_blueprint(user_bp, url_prefix="/user")
app.register_blueprint(admin_bp, url_prefix="/admin")
app.register_blueprint(main_bp, url_prefix="/main")

# try:
#     with app.app_context():
#         # Use text() to explicitly declare your SQL command
#         # result = db.session.execute(text("SELECT 1")).fetchall()
#         # print("Connection successful:", result)
#         db.drop_all()
#         db.create_all() # creates tables if they dont exist. Must be after model is created. Sync tables to DB
# except Exception as e:
#     print("Error connecting to the database:", e)