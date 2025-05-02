from flask import Flask, session, blueprints, request, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
import config
from app.routes.auth import auth_user
from app.routes.new_user import new_user
from app.models import Todo, User
from app.utils import login_required


db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    app.register_blueprint(auth_user, url_prefix="")
    app.register_blueprint(new_user, url_prefix="")
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
        
    @app.route("/dashboard")
    @login_required
    def dashboard():

        id = session['user_id']
        user = User.query.get_or_404(id)

        tasks = Todo.query.filter_by(user_id=user.id)
        return render_template("dashboard.html", tasks = tasks, username=user.username)


    @app.route("/logout", methods=['POST'])
    def logout():
        user_id = session['user_id']
        session.pop('user_id', None)
        return redirect(url_for('index'))


    with app.app_context():
        db.create_all()

    return app
