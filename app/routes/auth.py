from flask import Blueprint, redirect, request, session, url_for, render_template, flash
from app.utils import login_required
from werkzeug.security import  check_password_hash

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        from app.models import User
        username = request.form.get('username', "")
        password = request.form.get('password', "")
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid username or password", category="login_error")
            return redirect(url_for("auth.login"))
    else:
        return render_template("login.html")

    