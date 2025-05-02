from flask import redirect, url_for, session
from functools import wraps

def login_required(func):
    @wraps(func)
    def login_wrapper(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for("login"))
        return func(*args, **kwargs)
    return login_wrapper