from flask import Flask, session, blueprints, request, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy # type: ignore
from datetime import timedelta
import config
from app.routes.auth import auth
from app.routes.new_user import new_user
from app.routes.tasks import tasks
from app.utils import login_required
import os


db = SQLAlchemy()


def create_app():
    app = Flask(__name__, static_folder=os.path.join("..", "static"), template_folder=os.path.join("..", "templates"))
    app.config.from_object(config)
    db.init_app(app)

    from app.models import Todo, User

    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(new_user, url_prefix="/new_user")
    app.register_blueprint(tasks, url_prefix="/tasks")

    @app.route("/")
    def index():
        # return render_template("index.html")
        return redirect(url_for("auth.login"))


    @app.route("/register", methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            return redirect(url_for("new_user.new_user_register"))
        else:
            return render_template("register.html")
        
    @app.route("/dashboard")
    @login_required
    def dashboard():
        if "user_id" not in session:
             return redirect(url_for("auth.login"))
        
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
