from flask import Blueprint, render_template
from wtforms import StringField, SubmitField, IntegerField, SelectField, BooleanField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from models.policy_type import PolicyType

main_bp = Blueprint("main_bp", __name__)

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

@main_bp.route("/")
def home():
    return render_template("home.html", policyTypes=PolicyType.query.all())

@main_bp.route("/policy/<id>")
def policy(id):
    form = LegalInsuranceEstimateForm()
    policy_type = PolicyType.query.get(id)
    if policy:
        return render_template("policy.html", policy=policy_type, form=form)
    else:
        return f"Policy not found for ID: {id}", 404 
    
@main_bp.route("/quote")
def quote():
    return render_template("quote.html")