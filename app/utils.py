```python
from flask import url_for
from werkzeug.utils import redirect
from app.models import User
from flask_login import current_user

def redirect_url(default='index'):
    return request.args.get('next') or \
           request.referrer or \
           url_for(default)

def is_admin(user_id):
    user = User.query.get(user_id)
    if user is None:
        return False
    return user.is_admin

def is_doctor(user_id):
    user = User.query.get(user_id)
    if user is None:
        return False
    return user.is_doctor

def is_patient(user_id):
    user = User.query.get(user_id)
    if user is None:
        return False
    return user.is_patient

def current_user_is_admin():
    return is_admin(current_user.id)

def current_user_is_doctor():
    return is_doctor(current_user.id)

def current_user_is_patient():
    return is_patient(current_user.id)
```