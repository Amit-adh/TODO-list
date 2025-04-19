from flask import Flask, render_template, url_for, request, redirect, session # type: ignore
from flask_sqlalchemy import SQLAlchemy # type: ignore

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.secret_key = "A_random_secret_key"
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    tasks = db.relationship('Todo', backref='user', lazy=True)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    priority = db.Column(db.String(10), nullable=False)
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
        return redirect(url_for("new_user"))
    else:
        return render_template("register.html", err=False)


@app.route("/new_user", methods=['POST', 'GET'])
def new_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        re_pass = request.form['re-pass']
        
        if User.query.filter_by(username=username).first():
            return  render_template("register.html", err=True, err_msg="Username already exists")    
        
        if(password == re_pass):
            user = User(username=username, password=password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("login"))
        else:
            return render_template("register.html", err=True, err_msg="Both passwords must be the same")
        
    return render_template("register.html", err=False)


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
        return redirect(url_for("dashboard"))
    else:
        return redirect(url_for("login", err=True, err_msg="User does not exist in records."))


@app.route("/dashboard")
def dashboard():
    if 'user_id' not in session:
         return redirect(url_for('login'))

    id = session['user_id']
    user = User.query.get_or_404(id)

    tasks = Todo.query.filter_by(user_id=user.id)
    return render_template("dashboard.html", tasks = tasks)


@app.route("/logout", methods=['POST'])
def logout():
    user_id = session['user_id']
    session.pop('user_id', None)
    return redirect(url_for('index'))


@app.route("/add_task", methods=['POST'])
def add_task():
    if 'user_id' not in session:
        return redirect(url_for("login"))

    user_id = session['user_id']
    user = User.query.get_or_404(user_id)

    content = request.form['task-text'].strip()
    if content != "":
        priority = request.form['priority']
        task = Todo(content=content, priority=priority, user_id=user.id)
        db.session.add(task)
        db.session.commit()

    return redirect(url_for('dashboard'))


@app.route('/modify', methods=['POST', 'GET'])
def modify_task():
    if 'user_id' not in session:
         return redirect(url_for("index"))
    
    user_id = session['user_id']
    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        task_content = request.form['modified-text']
        task_id = session['curr_task']
        session.pop('curr_task', None)
        curr_task = Todo.query.filter_by(user_id=user.id, id=task_id).first()
        curr_task.content = task_content
        db.session.commit()

        tasks = Todo.query.filter_by(user_id = user.id)
        return redirect(url_for("dashboard", tasks=tasks))
    
    else:
        task_id = int(request.args['task_id'])
        session['curr_task'] = task_id
        curr_task = Todo.query.filter_by(user_id = user.id, id=task_id).first()
        return render_template("modify.html", task = curr_task)


@app.route('/delete', methods=['POST'])
def delete_task():
    if 'user_id' not in session:
         return redirect(url_for("index"))
    
    user_id = session['user_id']
    user = User.query.get_or_404(user_id)

    task_id = request.form['task_id']
    curr_task = Todo.query.get_or_404(task_id)

    db.session.delete(curr_task)
    db.session.commit()

    tasks = Todo.query.filter_by(user_id = user.id)
    return redirect(url_for("dashboard", tasks=tasks))

if __name__ == "__main__":
    app.run(debug=True)