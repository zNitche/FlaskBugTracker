from flask import Blueprint, render_template
import flask_login
from flask_bug_tracker.app_modules import decorators


admin = Blueprint("admin", __name__, template_folder="templates", static_folder="static", url_prefix="/admin")


@admin.route("/")
@flask_login.login_required
@decorators.admin_required
def home():
    return render_template("admin.html")
