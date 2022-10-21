from flask import Blueprint, render_template
import flask_login
from flask_bug_tracker import models
from flask_bug_tracker.consts import PaginationConsts


main_app = Blueprint("main_app", __name__, template_folder="templates", static_folder="static", url_prefix="/")


@main_app.route("/", defaults={"page_id": 1})
@main_app.route("/home/<int:page_id>")
@flask_login.login_required
def home(page_id):
    current_user_id = flask_login.current_user.id

    user_actions_logs_pagination = models.UserActionLog.get_actions_for_user_id(current_user_id)
    user_actions_logs_pagination = user_actions_logs_pagination.paginate(page=page_id,
                                                                         per_page=PaginationConsts.LOGS_PER_HOME_PAGE)

    return render_template("index.html",
                           user_actions_logs_pagination=user_actions_logs_pagination,
                           user_actions_logs=user_actions_logs_pagination.items)
