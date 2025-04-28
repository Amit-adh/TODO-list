from flask import Flask, session, blueprints, request, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from .. import config

app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)

def create_app():


    return app
