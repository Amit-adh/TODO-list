from flask import Blueprint, redirect, request, session, url_for, render_template
from app.utils import login_required

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        return redirect(url_for("auth.verify_user"))
    else:
        return render_template("login.html")

@auth.route("/verify_user", methods=["POST"])
@login_required
def verify_user():
    from app.models import User
    print("yes")
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username, password=password).first()
    if user:
        session['user_id'] = user.id
        return redirect(url_for("dashboard"))
    else:
        print("no")
        return redirect(url_for("auth.login", err=True, err_msg="User does not exist in records."))
    