from flask import Blueprint, render_template

about_bp = Blueprint("about_bp", __name__)

@about_bp.route("/contact")
def contact():
    return render_template("contact.html")