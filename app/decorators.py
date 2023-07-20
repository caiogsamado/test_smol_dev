from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user

def check_confirmed(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.confirmed is False:
            flash('Please confirm your account!', 'warning')
            return redirect(url_for('unconfirmed'))
        return func(*args, **kwargs)

    return decorated_function

def requires_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if current_user.role not in roles:
                flash('You do not have the required role to access this page.', 'danger')
                return redirect(url_for('index'))
            return f(*args, **kwargs)
        return wrapped
    return wrapper