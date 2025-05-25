import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'a3Dg2zhP2V3LD8kStBkr56nxZWWZS1p0')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///todo.db')

