from flask import request, render_template, redirect, url_for, Blueprint
import re

new_user = Blueprint("new_user", __name__)

@new_user.route("/", methods=['POST', 'GET'])
def new_user_register():
    if request.method == 'POST':
        from app import db
        from app.models import User
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        re_pass = request.form['re-pass']
        email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        
        if User.query.filter_by(username=username).first():
            return render_template("register.html", err=True, err_msg="Username already exists")    
        
        elif not re.match(email_pattern, email):
            return render_template("register.html", err=True, err_msg="Invalid Email", uname=username)
        
        elif  password != re_pass:
            return render_template("register.html", err=True, err_msg="Both passwords must be the same", uname=username, email=email)
        

        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("auth.login"))
    
    return render_template("register.html", err=False)
