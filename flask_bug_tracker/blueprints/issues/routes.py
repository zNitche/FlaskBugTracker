from flask import Blueprint, render_template, flash, redirect, url_for, request, abort
import flask_login
from datetime import datetime
from flask_bug_tracker import models
from flask_bug_tracker.app_modules import forms, decorators
from flask_bug_tracker.utils import db_utils, table_utils, issues_utils, logs_utils
from flask_bug_tracker.consts import SystemMessagesConst, FlashConsts, PaginationConsts, IssuesConsts


issues = Blueprint("issues", __name__, template_folder="templates", static_folder="static", url_prefix="/issues")


@issues.route("/")
@flask_login.login_required
def home():
    page_options = [
        {
            "content": "Add Issue",
            "url": url_for('issues.add_issue')
        },
        {
            "content": "My Issues",
            "url": url_for('issues.preview_my_issues')
        },
    ]

    if flask_login.current_user.is_admin():
        page_options.append({
            "content": "All Issues",
            "url": url_for('issues.preview_all_issues')
        })

    return render_template("navigation_page.html", page_options=page_options)


@issues.route("/all", defaults={"page_id": 1}, methods=["GET", "POST"])
@issues.route("/all/<int:page_id>", methods=["GET", "POST"])
@flask_login.login_required
@decorators.admin_required
def preview_all_issues(page_id):
    search_issue_form = forms.SearchIssueForm()

    issues = models.Issue.query.order_by(models.Issue.last_updated.desc())

    if search_issue_form.validate_on_submit() and search_issue_form.status.data != IssuesConsts.ALL_ISSUES:
        issues = issues.order_by(models.Issue.last_updated.desc()).filter_by(status=search_issue_form.status.data)

    issues = issues.paginate(page=page_id, per_page=PaginationConsts.ISSUES_PER_PAGE)

    table_struct = table_utils.get_data_table_data_struct_for_issues(issues.items)

    return render_template("preview_issues.html", issues=issues, table_struct=table_struct,
                           search_issue_form=search_issue_form)


@issues.route("/my", defaults={"page_id": 1}, methods=["GET", "POST"])
@issues.route("/my/<int:page_id>", methods=["GET", "POST"])
@flask_login.login_required
def preview_my_issues(page_id):
    current_user_id = flask_login.current_user.id
    search_issue_form = forms.SearchIssueForm()

    issues = models.Issue.query.order_by(models.Issue.last_updated.desc()).filter(
        (models.Issue.owner_id == current_user_id) | (models.Issue.assigned_to_user_id == current_user_id))

    if search_issue_form.validate_on_submit() and search_issue_form.status.data != IssuesConsts.ALL_ISSUES:
        issues = issues.order_by(models.Issue.last_updated.desc()).filter_by(status=search_issue_form.status.data)

    issues = issues.paginate(page=page_id, per_page=PaginationConsts.ISSUES_PER_PAGE)

    table_struct = table_utils.get_data_table_data_struct_for_issues(issues.items)

    return render_template("preview_issues.html", issues=issues, table_struct=table_struct,
                           search_issue_form=search_issue_form)


@issues.route("/issue/<issue_id>", methods=["GET"])
@flask_login.login_required
def preview_issue(issue_id):
    issue = models.Issue.query.filter_by(id=issue_id).first()

    if issue and (issues_utils.check_issue_access(issue, flask_login.current_user) or
                  flask_login.current_user.id == issue.assigned_to_user_id):

        issue_form = forms.UpdateIssueForm(issue.id)

        issue_form.title.data = issue.title
        issue_form.content.data = issue.content
        issue_form.status.data = issue.status

        issue_form.assigned_to_user_name.choices = [user.username for user in models.User.query.all()]
        issue_form.assigned_to_user_name.data = issue.get_assigned_to_user_name()

        return render_template("issue.html", issue=issue, issue_form=issue_form)

    else:
        abort(404)


@issues.route("/issue/<issue_id>/update", methods=["POST"])
@flask_login.login_required
def update_issue(issue_id):
    issue = models.Issue.query.filter_by(id=issue_id).first()
    current_user = flask_login.current_user

    if issue and issues_utils.check_issue_access(issue, flask_login.current_user):
        issue_form = forms.UpdateIssueForm(issue.id)

        issue_form.assigned_to_user_name.choices = [user.username for user in models.User.query.all()]

        if issue_form.validate_on_submit():
            issue.title = issue_form.title.data
            issue.content = issue_form.content.data
            issue.last_updated = datetime.utcnow()

            assigned_user_id = models.User.query.filter_by(username=issue_form.assigned_to_user_name.data).first().id

            if not issue.assigned_to_user_id == assigned_user_id:
                logs_utils.log_issue_assignment_change(current_user, issue, issue_form.assigned_to_user_name.data)

            if not issue.status == issue_form.status.data:
                logs_utils.log_issue_status_change(current_user, issue, issue_form.status.data)

            issue.status = issue_form.status.data
            issue.assigned_to_user_id = assigned_user_id

            db_utils.commit_session()

            flash(SystemMessagesConst.ISSUE_UPDATED, FlashConsts.FLASH_SUCCESS)

        else:
            flash(SystemMessagesConst.ERROR_WHILE_UPDATING_ISSUE, FlashConsts.FLASH_DANGER)

            return render_template("issue.html", issue=issue, issue_form=issue_form)

        return redirect(url_for("issues.preview_issue", issue_id=issue_id))

    else:
        abort(404)


@issues.route("/issue/<issue_id>/remove", methods=["POST"])
@flask_login.login_required
def remove_issue(issue_id):
    issue = models.Issue.query.filter_by(id=issue_id).first()

    if issue and issues_utils.check_issue_access(issue, flask_login.current_user):
        db_utils.remove_object_from_db(issue)

        flash(SystemMessagesConst.ISSUE_REMOVED, FlashConsts.FLASH_SUCCESS)

        return redirect(url_for("issues.preview_my_issues"))

    else:
        abort(404)


@issues.route("/add", methods=["GET", "POST"])
@flask_login.login_required
def add_issue():
    add_issue_form = forms.AddIssueForm()
    add_issue_form.assigned_to_user_name.choices = [user.username for user in models.User.query.all()]

    user = flask_login.current_user

    if add_issue_form.validate_on_submit():
        title = add_issue_form.title.data
        content = add_issue_form.content.data
        assigned_to_user_name = add_issue_form.assigned_to_user_name.data

        assigned_to_user_id = models.User.query.filter_by(username=assigned_to_user_name).first().id

        issue = models.Issue(title=title, content=content, assigned_to_user_id=assigned_to_user_id,
                             owner_id=user.id)

        db_utils.add_object_to_db(issue)

        logs_utils.log_issue_assignment_change(user, issue, assigned_to_user_name)

        flash(SystemMessagesConst.ADDED_ISSUE, FlashConsts.FLASH_SUCCESS)

    elif not add_issue_form.validate_on_submit() and request.method == "POST":
        flash(SystemMessagesConst.ERROR_WHILE_ADDING_ISSUE, FlashConsts.FLASH_DANGER)

    if request.method == "POST":
        return redirect(url_for("issues.preview_my_issues"))

    return render_template("add_issue.html", add_issue_form=add_issue_form)
