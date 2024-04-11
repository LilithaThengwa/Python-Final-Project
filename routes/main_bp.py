from flask_login import login_required
from sqlalchemy import func
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
import matplotlib.pyplot as plt
import io
import base64

from routes.user_bp import role_required

main_bp = Blueprint("main_bp", __name__)