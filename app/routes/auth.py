from flask import Blueprint, redirect, request, session, url_for, render_template
from . import login_required
from ..models import User

auth = Blueprint("auth", __name__, static_folder="static", template_folder="templates")

@auth.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        return redirect(url_for("auth_user"))
    else:
        return render_template("login.html")

@auth.route("/auth_user", methods=["POST"])
@login_required
def auth_user():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username, password=password).first()
    if user:
        session['user_id'] = user.id
        return redirect(url_for("dashboard"))
    else:
        return redirect(url_for("login", err=True, err_msg="User does not exist in records."))
    