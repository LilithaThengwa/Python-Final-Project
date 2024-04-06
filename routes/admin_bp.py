from extensions import db
from flask import flash
from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from wtforms.validators import InputRequired, Email, Length
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, Length, ValidationError, DataRequired
from datetime import date
from flask_wtf import FlaskForm
from models.customer import Customer
from models.policy import Policies
from models.claim import Claims
from models.policy_type import PolicyType

admin_bp = Blueprint("admin_bp", __name__)

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


@admin_bp.route("/")
def admin_dashboard():
    return render_template("admindashboard.html")

@admin_bp.route("/customers")
def customer_list():
    return render_template("customer-management.html", customers=Customer.query.all())

@admin_bp.route("/policies")
def policy_list():
    return render_template("policy-management.html", customers=Customer.query.all(), policy_types=PolicyType.query.all())

@admin_bp.route("/update-customer", methods=["POST"])
def show_update_customer():
    customerID = request.form.get("CustomerID")

    customer = Customer.query.get(customerID)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404

    form = UpdateCustomerForm(obj=customer)  # Prepopulate form with customer data
    return render_template("update-customer.html", form=form, customer=customer)

@admin_bp.route("/update-customer/<CustomerID>", methods=["GET", "POST"])
def update_customer_info(CustomerID):
    customer = Customer.query.get(CustomerID)
    print(customer)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404

    form = UpdateCustomerForm(request.form, obj=customer)  # Prepopulate form with customer data

    if form.validate_on_submit():
        customer.FirstName = form.FirstName.data
        customer.LastName = form.LastName.data
        customer.Email = form.Email.data
        customer.PhoneNumber = form.PhoneNumber.data

        try:
            db.session.commit()
            return jsonify({"message": "Customer information updated successfully", "data": customer.to_dict()}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500

    # If the form is not submitted or not valid, render the update-customer.html template with the prepopulated form
    return render_template("update-customer.html", customer=customer, form=form)

@admin_bp.route("/update-policy-type", methods=["POST"])
def show_update_policy_type():
    policyTypeID = request.form.get("PolicyTypeID")

    policy_type = PolicyType.query.get(policyTypeID)
    if not policy_type:
        return jsonify({"error": "Policy type not found"}), 404

    form =  UpdatePolicyTypeForm(obj=policy_type)  # Prepopulate form with customer data
    return render_template("update-policy-type.html", form=form, policy_type=policy_type)

@admin_bp.route("/update-policy-type/<PolicyTypeID>", methods=["GET", "POST"])
def update_policy_info(PolicyTypeID):
    policy_type = PolicyType.query.get(PolicyTypeID)
    print(policy_type)
    if not policy_type:
        return jsonify({"error": "Policy not found"}), 404

    form = UpdatePolicyTypeForm(request.form, obj=policy_type)  # Prepopulate form with customer data

    if form.validate_on_submit():
        policy_type.name = form.name.data
        policy_type.description = form.description.data
        policy_type.short_description = form.short_description.data
        policy_type.img = form.img.data
        policy_type.alt = form.alt.data

        try:
            db.session.commit()
            return jsonify({"message": "Customer information updated successfully", "data": policy_type.to_dict()}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500

    # If the form is not submitted or not valid, render the update-customer.html template with the prepopulated form
    return render_template("update-policy-type.html", policy_type=policy_type, form=form)


@admin_bp.route("/claims")
def view_claims():
    pending_claims = Claims.query.filter_by(Status='Pending').all()
    return render_template("claims-processing.html", pending_claims=pending_claims)

@admin_bp.route("/process-claim/<ClaimID>", methods=["GET", "POST"])
def process_claim(ClaimID):
    claim = Claims.query.get(ClaimID)
    if not claim:
        return "Claim not found", 404

    if request.method == "POST":
        new_status = request.form['status']
        claim.Status = new_status
        db.session.commit()
        return redirect(url_for('admin_bp.view_claims'))

    return render_template("process_claim.html", claim=claim)