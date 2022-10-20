from flask import Blueprint, render_template, flash, redirect, url_for, request, abort
import flask_login
from datetime import datetime
from flask_bug_tracker import models
from flask_bug_tracker.app_modules import forms
from flask_bug_tracker.utils import db_utils, table_utils
from flask_bug_tracker.consts import SystemMessagesConst, FlashConsts


issues = Blueprint("issues", __name__, template_folder="templates", static_folder="static", url_prefix="/issues")


@issues.route("/")
@flask_login.login_required
def preview_issues():
    issues = models.Issue.query.all()

    table_struct = table_utils.get_data_table_data_struct_for_issues(issues)

    return render_template("issues.html", table_struct=table_struct)


@issues.route("/issue/<issue_id>", methods=["GET"])
@flask_login.login_required
def preview_issue(issue_id):
    issue = models.Issue.query.filter_by(id=issue_id).first()

    if issue:
        issue_form = forms.AddIssueForm()

        issue_form.title.data = issue.title
        issue_form.content.data = issue.content

        issue_form.assigned_to_user_name.choices = [user.username for user in models.User.query.all()]
        issue_form.assigned_to_user_name.data = issue.get_assigned_to_user_name()

        return render_template("issue.html", issue=issue, issue_form=issue_form)

    else:
        abort(404)


@issues.route("/issue/<issue_id>/update", methods=["POST"])
@flask_login.login_required
def update_issue(issue_id):
    issue = models.Issue.query.filter_by(id=issue_id).first()

    if issue and issue.owner_id == flask_login.current_user.id:
        issue_form = forms.AddIssueForm()

        issue_form.assigned_to_user_name.choices = [user.username for user in models.User.query.all()]

        if issue_form.validate_on_submit():
            issue.title = issue_form.title.data
            issue.content = issue_form.content.data
            issue.last_updated = datetime.utcnow()

            issue.assigned_to_user_id = \
                models.User.query.filter_by(username=issue_form.assigned_to_user_name.data).first().id

            db_utils.commit_session()

            flash(SystemMessagesConst.ISSUE_UPDATED, FlashConsts.FLASH_SUCCESS)

        else:
            flash(SystemMessagesConst.ERROR_WHILE_UPDATING_ISSUE, FlashConsts.FLASH_DANGER)

        return redirect(url_for("issues.preview_issue", issue_id=issue_id))

    else:
        abort(404)


@issues.route("/issue/<issue_id>/remove", methods=["POST"])
@flask_login.login_required
def remove_issue(issue_id):
    issue = models.Issue.query.filter_by(id=issue_id).first()

    if issue and issue.owner_id == flask_login.current_user.id:
        db_utils.remove_object_from_db(issue)

        flash(SystemMessagesConst.ISSUE_REMOVED, FlashConsts.FLASH_SUCCESS)

        return redirect(url_for("issues.preview_issues"))

    else:
        abort(404)


@issues.route("/add", methods=["GET", "POST"])
@flask_login.login_required
def add_issue():
    add_issue_form = forms.AddIssueForm()
    add_issue_form.assigned_to_user_name.choices = [user.username for user in models.User.query.all()]

    if add_issue_form.validate_on_submit():
        title = add_issue_form.title.data
        content = add_issue_form.content.data
        assigned_to_user_name = add_issue_form.assigned_to_user_name.data

        assigned_to_user_id = models.User.query.filter_by(username=assigned_to_user_name).first().id

        issue = models.Issue(title=title, content=content, assigned_to_user_id=assigned_to_user_id,
                             owner_id=flask_login.current_user.id)

        db_utils.add_object_to_db(issue)

        flash(SystemMessagesConst.ADDED_ISSUE, FlashConsts.FLASH_SUCCESS)

    elif not add_issue_form.validate_on_submit() and request.method == "POST":
        flash(SystemMessagesConst.ERROR_WHILE_ADDING_ISSUE, FlashConsts.FLASH_DANGER)

    if request.method == "POST":
        return redirect(url_for("issues.preview_issues"))

    return render_template("add_issue.html", add_issue_form=add_issue_form)
