from flask import Flask, render_template, url_for, request # type: ignore
from flask_sqlalchemy import SQLAlchemy # type: ignore

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
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



@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        return render_template("login.html")
    else:
        return render_template("index.html")


# @app.route("/dashboard/<str:name>", methods=['POST', 'GET'])
# def dashboard(name):
#     if request.method == 'POST':
#         pass
#     else:
#         return name + "hello"



if __name__ == "__main__":
    app.run(debug=True)