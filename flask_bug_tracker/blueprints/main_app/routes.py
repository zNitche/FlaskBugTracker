from flask import Blueprint, render_template
import flask_login
from flask_bug_tracker import models


main_app = Blueprint("main_app", __name__, template_folder="templates", static_folder="static", url_prefix="/")


@main_app.route("/")
@flask_login.login_required
def home():
    current_user_id = flask_login.current_user.id

    user_actions_logs = models.UserActionLog.get_actions_for_user_id(current_user_id)

    return render_template("index.html", user_actions_logs=user_actions_logs)
