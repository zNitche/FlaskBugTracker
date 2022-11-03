import pytest
from flask import url_for
import os
from flask_bug_tracker import models
from flask_bug_tracker.consts import PermissionGroupsConsts, IssuesConsts
from flask_bug_tracker import create_app
from tests.test_config import TestConfig


@pytest.fixture(scope="module")
def new_admin_user():
    user = models.User(username="test_admin_user", email="test_admin_user@email.com", password="test_password",
                       permission_group_id=PermissionGroupsConsts.ADMIN_GROUP_ID)

    return user


@pytest.fixture(scope="module")
def new_regular_user():
    user = models.User(username="test_user", email="test_user@email.com", password="test_password",
                       permission_group_id=PermissionGroupsConsts.USER_GROUP_ID)

    return user


@pytest.fixture(scope="module")
def new_permission_group():
    group = models.PermissionGroup(name="test_group")

    return group


@pytest.fixture(scope="module")
def new_issue():
    issue = models.Issue(title="test_issue",
                         content="test content",
                         status=IssuesConsts.ISSUE_TODO,
                         owner_id=1,
                         project_id=1)

    return issue


@pytest.fixture(scope="module")
def new_project():
    project = models.Project(name="test_project",
                             owner_id=1)

    return project


@pytest.fixture(scope="module")
def test_client():
    flask_app = create_app(TestConfig)
    client = flask_app.test_client()

    with flask_app.test_request_context():
        yield client


@pytest.fixture(scope="module")
def logged_test_user(test_client):
    from flask_bug_tracker.app_modules import forms

    form = forms.LoginForm()
    form.email.data = os.environ.get("BUILD_IN_ADMIN_USERNAME")
    form.password.data = os.environ.get("BUILD_IN_ADMIN_PASSWORD")

    test_client.post(url_for("auth.login"), data=form.data, follow_redirects=True)

    yield test_client

    test_client.get(url_for("auth.logout"), follow_redirects=True)
