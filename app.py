from flask import Flask, render_template, url_for, request # type: ignore
from flask_sqlalchemy import SQLAlchemy # type: ignore

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Todo {self.id} - {self.content}>'
    
with app.app_context():
    db.create_all()



@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        pass
    else:
        return render_template("index.html")


@app.route("/dashboard/<str:name>", methods=['POST', 'GET'])
def dashboard(name):
    if request.method == 'POST':
        pass



if __name__ == "__main__":
    app.run(debug=True)