from flask import current_app
from flask_bug_tracker import models
from flask_bug_tracker.utils import db_utils
from flask_bug_tracker.consts import UserActionsLogsConsts


def log_user_action(user_id, message, another_user_id=None):
    if not current_app.config["TESTING"]:
        # if user_id != another_user_id:
        log = models.UserActionLog(user_id=user_id, content=message, another_user_id=another_user_id)

        db_utils.add_object_to_db(log)


def log_issue_assignment_change(current_user, issue, assignee_name):
    if not current_app.config["TESTING"]:
        log_user_action(current_user.id, UserActionsLogsConsts.ISSUE_ASSIGNED_TO_USER.format(
            issue_id=str(issue.id),
            assignee_name=assignee_name,
            reporter_name=current_user.username
        ), issue.assigned_to_user_id)


def log_issue_status_change(current_user, issue, issue_status):
    if not current_app.config["TESTING"]:
        log_user_action(current_user.id, UserActionsLogsConsts.ISSUE_STATUS_CHANGED.format(
            issue_id=str(issue.id),
            issue_state=issue_status,
            username=current_user.username
        ), issue.assigned_to_user_id)
