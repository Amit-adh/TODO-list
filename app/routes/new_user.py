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

        errors = {}
        
        if User.query.filter_by(username=username).first():
            flash("username_error")
            errors["username_error"] = True
        
        if User.query.filter_by(email=email).first():   
            flash("email_unique_error")
            errors["email_unique_error"] = True

        if not re.match(email_pattern, email):
            flash("email_error")
            errors["email_error"] = True
        
        if password != re_pass:
            flash("different_passwords")
            errors["different_passwords"] = True
        if errors:
            # for cat, msg in errors.items():
            #     flash(msg, category=cat)
            return render_template("register.html", uname=username, email=email)
        

        user = User(username=username, email=email)
        user.password = user.generate_password(password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("auth.login"))
    
    return render_template("register.html")
