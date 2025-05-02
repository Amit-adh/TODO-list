from flask import Flask, session, blueprints, request, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from .. import config
from routes.auth import auth_user
import models

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    app.register_blueprint(auth_user, url_prefix="")
    db.init_app(app)

    @app.route("/")
    def index():
            return render_template("index.html")


    @app.route("/register", methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            return redirect(url_for("new_user"))
        else:
            return render_template("register.html")


    with app.app_context():
        db.create_all()

    return app
