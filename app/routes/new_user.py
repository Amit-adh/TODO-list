from flask import request, render_template, redirect, url_for, Blueprint, flash
import re

new_user = Blueprint("new_user", __name__)

@new_user.route("/", methods=['POST', 'GET'])
def new_user_register():
    if request.method == 'POST':
        from app import db
        from app.models import User
        username = request.form.get("username", "")
        email = request.form.get("email", "")
        password = request.form.get("password", "")
        re_pass = request.form.get("repass", "")
        email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        
        if User.query.filter_by(username=username).first():
            flash("Username already exists", category="username_error")
            return render_template("register.html")    
        
        elif not re.match(email_pattern, email):
            flash("Invalid Email", category="email_error")
            return render_template("register.html", uname=username)
        
        elif password == "":
            flash("Password must not be empty", category="empty_password")
            return render_template("register.html", uname=username, email=email)
        
        elif password != re_pass:
            flash("Both passwords must be the same", category="different_passwords")
            return render_template("register.html", uname=username, email=email)
        

        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("auth.login"))
    
    return render_template("register.html")
