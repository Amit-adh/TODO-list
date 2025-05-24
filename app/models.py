from werkzeug.security import generate_password_hash, check_password_hash

def get_db():
    from app import db
    return db
class User(get_db().Model):
    db = get_db()
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    tasks = db.relationship('Todo', backref='user', lazy=True)

    def __repr__(self):
        return f"<User: {self.username}>"
    
    def generate_password(self, password):
        return generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Todo(get_db().Model):
    db = get_db()
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    priority = db.Column(db.String(10), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"<Task: {self.content}\tPriority: {self.priority}>"
    