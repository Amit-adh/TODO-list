from flask import Flask, render_template, url_for, request, redirect, session # type: ignore
from flask_sqlalchemy import SQLAlchemy # type: ignore

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.secret_key = "your_very_secret_key_here"
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    tasks = db.relationship('Todo', backref='user', lazy=True)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Todo {self.id} - {self.content}>'
    
with app.app_context():
    db.create_all()



@app.route("/")
def index():
        return render_template("index.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        return redirect(url_for("login"))
    else:
        return render_template("register.html")

@app.route("/new_user", methods=['POST'])
def add_user():
    username = request.form['username']
    password = request.form['password']
    re_pass = request.form['re-pass']
    
    if(password == re_pass):
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))
    else:
        return "Both passwords must be the same"

@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        return redirect(url_for("auth_user"))
    else:
        return render_template("login.html")

@app.route("/auth_user", methods=['POST'])
def auth_user():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username, password=password).first()
    if user:
        session['user_id'] = user.id
        return redirect(url_for("dashboard", id = user.id))
    else:
        return "User doesn't exist in records"


@app.route("/dashboard/<int:id>", methods=['GET', 'POST'])
def dashboard(id):
    user = User.query.get_or_404(id)
    if request.method == 'POST':
        return "registered"
    else:
        return render_template("dashboard.html", user=user)

@app.route("/logout", methods=['POST'])
def logout():
    user_id = session['user_id']
    session.pop(user_id, None)
    return redirect(url_for('login'))

@app.route("/add_task")
def add_task():
    return "added task"

if __name__ == "__main__":
    app.run(debug=True)