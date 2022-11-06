import flask_login
from flask import url_for
from flask_bug_tracker import models


def test_issues_preview_as_user(test_client, logged_test_user):
    response = test_client.get(url_for("issues.preview_all_issues"), follow_redirects=True)

    assert response.status_code == 403


def test_issues_preview_as_admin(test_client, logged_test_admin):
    response = test_client.get(url_for("issues.preview_all_issues"), follow_redirects=True)

    assert response.status_code == 200
    assert response.request.path == url_for("issues.preview_all_issues")


def test_preview_my_issues(test_client, logged_test_user):
    response = test_client.get(url_for("issues.preview_my_issues"), follow_redirects=True)

    assert response.status_code == 200
    assert response.request.path == url_for("issues.preview_my_issues")


def test_add_issue(test_client, logged_test_user, new_issue, new_project):
    from flask_bug_tracker.app_modules import forms
    from flask_bug_tracker.utils import db_utils

    response = test_client.get(url_for("issues.add_issue"), follow_redirects=True)

    assert response.status_code == 200
    assert response.request.path == url_for("issues.add_issue")

    new_project.members.append(flask_login.current_user)
    db_utils.add_object_to_db(new_project)

    project = models.Project.query.filter_by(name=new_project.name).first()

    assert project

    add_issue_form = forms.AddIssueForm()

    add_issue_form.title.data = new_issue.title
    add_issue_form.content.data = new_issue.content
    add_issue_form.assigned_to_user_name.data = flask_login.current_user.username
    add_issue_form.project_name.data = project.name

    response = test_client.post(url_for("issues.add_issue"), data=add_issue_form.data, follow_redirects=True)
    assert response.status_code == 200

    issue = models.Issue.query.filter_by(title=new_issue.title).first()

    assert issue


def test_preview_issue(test_client, logged_test_user):
    response = test_client.get(url_for("issues.preview_issue", issue_id=1), follow_redirects=True)

    assert response.status_code == 200
    assert response.request.path == url_for("issues.preview_issue", issue_id=1)
