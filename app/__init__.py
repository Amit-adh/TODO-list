from flask import Flask, session, blueprints, request, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.confit['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)
app.secret_key = "A_random_secret_key"
db = SQLAlchemy(app)

def create_app():


    return app
