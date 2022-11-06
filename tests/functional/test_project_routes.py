from flask import url_for
from flask_bug_tracker import models


def test_projects_preview_as_user(test_client, logged_test_user):
    response = test_client.get(url_for("projects.preview_all_projects"), follow_redirects=True)

    assert response.status_code == 403


def test_projects_preview_as_admin(test_client, logged_test_admin):
    response = test_client.get(url_for("projects.preview_all_projects"), follow_redirects=True)

    assert response.status_code == 200
    assert response.request.path == url_for("projects.preview_all_projects")


def test_preview_my_projects(test_client, logged_test_user):
    response = test_client.get(url_for("projects.preview_my_projects"), follow_redirects=True)

    assert response.status_code == 200
    assert response.request.path == url_for("projects.preview_my_projects")


def test_add_project(test_client, logged_test_user, new_project):
    from flask_bug_tracker.app_modules import forms

    response = test_client.get(url_for("projects.add_project"), follow_redirects=True)

    assert response.status_code == 200
    assert response.request.path == url_for("projects.add_project")

    add_project_form = forms.AddProjectForm()

    add_project_form.name.data = new_project.name

    response = test_client.post(url_for("projects.add_project"), data=add_project_form.data, follow_redirects=True)
    assert response.status_code == 200

    project = models.Project.query.filter_by(name=new_project.name).first()

    assert project
