from flask_login import current_user, login_required
from sqlalchemy import func
from extensions import db
from flask import flash, session
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
import matplotlib.pyplot as plt
import io
import base64

from routes.user_bp import role_required

admin_bp = Blueprint("admin_bp", __name__)

class UpdateCustomerForm(FlaskForm):
    FirstName = StringField("First Name", validators=[InputRequired(), Length(max=50)])
    LastName = StringField("Last Name", validators=[InputRequired(), Length(max=50)])
    Email = StringField("Email", validators=[InputRequired(), Email(), Length(max=50)])
    PhoneNumber = StringField("Phone Number", validators=[InputRequired(), Length(max=20)])
    submit = SubmitField("Update")

class UpdatePolicyTypeForm(FlaskForm):
    name = StringField("Name", validators=[InputRequired(), Length(max=50)])
    description = TextAreaField("Description", validators=[InputRequired(), Length(max=500)])
    short_description = TextAreaField("Short Description", validators=[InputRequired(), Length(max=500)])
    img = StringField("Image URL", validators=[InputRequired(), Length(max=255)])
    alt = StringField("Alt Text", validators=[InputRequired(), Length(max=50)])
    submit = SubmitField("Update")


@admin_bp.route("/")
@login_required
@role_required("admin")
def admin_dashboard():
    bar_chart = policies_per_policy_type()
    line_chart = policies_per_policy_type_line()
    return render_template("admindashboard.html", bar_chart=bar_chart, line_chart=line_chart)

@admin_bp.route("/customers")
@login_required
@role_required("admin")
def customer_list():
    return render_template("customer-management.html", customers=Customer.query.all())

@admin_bp.route("/policies")
@login_required
@role_required("admin")
def policy_list():
    return render_template("policy-management.html", customers=Customer.query.all(), policy_types=PolicyType.query.all())

@admin_bp.route("/update-customer", methods=["POST"])
@login_required
def show_update_customer():
    customerID = request.form.get("CustomerID")

    customer = Customer.query.get(customerID)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404

    form = UpdateCustomerForm(obj=customer)  # Prepopulate form with customer data
    return render_template("update-customer.html", form=form, customer=customer)

@admin_bp.route("/update-customer/<CustomerID>", methods=["GET", "POST"])
@login_required
def update_customer_info(CustomerID):
    customer = Customer.query.get(CustomerID)
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
            flash(f"{customer.FirstName} {customer.LastName} information updated successfully")
            if current_user.role == "admin":
               print("proper")
               return redirect(url_for("admin_bp.customer_list")), 200
            return redirect(url_for("user_bp.customer_dashboard")), 200
        except Exception as e:
            db.session.rollback()
            flash({"error": str(e)})
            return render_template("update-customer.html", customer=customer, form=form), 500

    return render_template("update-customer.html", customer=customer, form=form)

@admin_bp.route("/update-policy-type", methods=["POST"])
@login_required
@role_required("admin")
def show_update_policy_type():
    policyTypeID = request.form.get("PolicyTypeID")

    policy_type = PolicyType.query.get(policyTypeID)
    if not policy_type:
        return jsonify({"error": "Policy type not found"}), 404

    form =  UpdatePolicyTypeForm(obj=policy_type)  # Prepopulate form with customer data
    return render_template("update-policy-type.html", form=form, policy_type=policy_type)

@admin_bp.route("/update-policy-type/<PolicyTypeID>", methods=["GET", "POST"])
@login_required
@role_required("admin")
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
            flash(f"{policy_type.name} information updated successfully")
            return redirect(url_for("admin_bp.policy_list")), 200
        except Exception as e:
            db.session.rollback()
            flash({"error": str(e)})
            return render_template("update-policy-type.html", policy_type=policy_type, form=form), 500

    return render_template("update-policy-type.html", policy_type=policy_type, form=form)

@admin_bp.route("/claims")
@login_required
@role_required("admin")
def view_claims():
    unresolved = ["Pending", "Investigating"]
    pending_claims = Claims.query.filter(Claims.Status.in_(unresolved)).all()
    return render_template("claims-processing.html", pending_claims=pending_claims)

@admin_bp.route("/process-claim/<ClaimID>", methods=["GET", "POST"])
@login_required
@role_required("admin")
def process_claim(ClaimID):
    claim = Claims.query.get(ClaimID)
    if not claim:
        return "Claim not found", 404

    if request.method == "POST":
        new_status = request.form["status"]
        claim.Status = new_status
        try:
            claim.Status = new_status
            db.session.commit()
            flash("Successful status update.")
            return redirect(url_for("admin_bp.view_claims"))
        except Exception as e:
            db.session.rollback()
            flash(f"Failed status update. Error: {str(e)}")
            return redirect(url_for("admin_bp.view_claims"))

    return render_template("process_claim.html", claim=claim)


def policies_per_policy_type():
    policy_type_counts = db.session.query(Policies.PolicyTypeID, func.count(Policies.PolicyID)).group_by(Policies.PolicyTypeID).all()

    policy_type_names = []
    policy_type_counts_list = []

    for policy_type_id, count in policy_type_counts:
        policy_type = PolicyType.query.get(policy_type_id)
        policy_type_names.append(policy_type.name)
        policy_type_counts_list.append(count)

    plt.figure(figsize=(10, 6))
    plt.bar(policy_type_names, policy_type_counts_list, color="grey")
    plt.title("Policies per Policy Type")
    plt.xlabel("Policy Type")
    plt.ylabel('Number of Policies')
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()

    bar_buffer = io.BytesIO()
    plt.savefig(bar_buffer, format="png")
    bar_buffer.seek(0)
    bar_chart_data = base64.b64encode(bar_buffer.getvalue()).decode()

    return bar_chart_data

def policies_per_policy_type_line():
    policy_type_counts = db.session.query(Policies.PolicyTypeID, func.count(Policies.PolicyID)).group_by(Policies.PolicyTypeID).all()

    policy_type_names = []
    policy_type_counts_list = []

    for policy_type_id, count in policy_type_counts:
        policy_type = PolicyType.query.get(policy_type_id)
        policy_type_names.append(policy_type.name)
        policy_type_counts_list.append(count)

    plt.figure(figsize=(10, 6))
    plt.plot(policy_type_names, policy_type_counts_list, marker='o', color='blue', linestyle='-', label="Line Graph")
    plt.title("Policies per Policy Type")
    plt.xlabel("Policy Type")
    plt.ylabel('Number of Policies')
    plt.xticks(rotation=30, ha="right")
    plt.legend()
    plt.tight_layout()

    line_buffer = io.BytesIO()
    plt.savefig(line_buffer, format="png")
    line_buffer.seek(0)
    line_chart_data = base64.b64encode(line_buffer.getvalue()).decode()

    return line_chart_data