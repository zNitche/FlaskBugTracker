from flask_bug_tracker import models
from flask_bug_tracker.utils import db_utils


def log_user_action(user_id, message, another_user_id=None):
    # if user_id != another_user_id:
    log = models.UserActionLog(user_id=user_id, content=message, another_user_id=another_user_id)

    db_utils.add_object_to_db(log)
