from flask import Blueprint, session, request, redirect, url_for, render_template
from ..models import Todo, User
from app.utils import login_required
from app import db

tasks = Blueprint("tasks", __name__)


@tasks.route("/add_task", methods=['POST'])
@login_required
def add_task():
    user_id = session['user_id']
    user = User.query.get_or_404(user_id)

    content = request.form['task-text'].strip()
    if content != "":
        priority = request.form['priority']
        task = Todo(content=content, priority=priority, user_id=user.id)

        db.session.add(task)
        db.session.commit()

    return redirect(url_for('dashboard'))


@tasks.route('/modify', methods=['POST', 'GET'])
@login_required
def modify_task():
    user_id = session['user_id']
    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        task_id = session['curr_task']
        session.pop('curr_task', None)
        db.session.commit()

        task_content = request.form['modified-text']
        curr_task = Todo.query.filter_by(user_id=user.id, id=task_id).first()
        curr_task.content = task_content
        
        tasks = Todo.query.filter_by(user_id = user.id)
        return redirect(url_for("dashboard", tasks=tasks))
    
    else:
        task_id = int(request.args['task_id'])
        session['curr_task'] = task_id
        curr_task = Todo.query.filter_by(user_id = user.id, id=task_id).first()

        return render_template("modify.html", task = curr_task)


@tasks.route('/delete', methods=['POST'])
@login_required
def delete_task():
    user_id = session['user_id']
    user = User.query.get_or_404(user_id)

    task_id = request.form['task_id']
    curr_task = Todo.query.get_or_404(task_id)

    db.session.delete(curr_task)
    db.session.commit()

    tasks = Todo.query.filter_by(user_id = user.id)
    return redirect(url_for("dashboard", tasks=tasks))
