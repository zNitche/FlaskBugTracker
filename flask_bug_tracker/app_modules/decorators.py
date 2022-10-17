from functools import wraps
from flask import request, redirect, url_for, abort
import flask_login


def admin_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if False:
            abort(404)

        return func(*args, **kwargs)

    return decorated_function
