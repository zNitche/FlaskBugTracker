from flask import Blueprint, render_template
import flask_login
from flask_bug_tracker import models


main_app = Blueprint("main_app", __name__, template_folder="templates", static_folder="static", url_prefix="/")


@main_app.route("/")
@flask_login.login_required
def home():
    current_user_id = flask_login.current_user.id

    my_issues = models.Issue.query.order_by(models.Issue.last_updated.desc()).filter(
        (models.Issue.owner_id == current_user_id) | (models.Issue.assigned_to_user_id == current_user_id)).all()

    return render_template("index.html", my_issues=my_issues)
