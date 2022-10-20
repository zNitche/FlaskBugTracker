from flask import Blueprint, render_template, flash, redirect, url_for, request
import flask_login
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
