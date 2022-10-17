from functools import wraps
from flask import abort
import flask_login


def admin_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not flask_login.current_user.is_admin():
            abort(403)

        return func(*args, **kwargs)

    return decorated_function
