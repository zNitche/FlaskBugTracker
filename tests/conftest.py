import pytest
from flask import url_for
import os
from flask_bug_tracker import models, db
from flask_bug_tracker.utils import account_utils
from flask_bug_tracker.consts import PermissionGroupsConsts, IssuesConsts
from flask_bug_tracker import create_app
from tests.test_config import TestConfig
from tests.consts import UsersConsts


@pytest.fixture(scope="function")
def new_admin_user():
    user = models.User(username=UsersConsts.TEST_ADMIN_USER_NAME,
                       email=UsersConsts.TEST_ADMIN_USER_EMAIL,
                       password=UsersConsts.TEST_ADMIN_USER_PASSWORD,
                       permission_group_id=PermissionGroupsConsts.ADMIN_GROUP_ID)

    return user


@pytest.fixture(scope="function")
def new_regular_user():
    user = models.User(username=UsersConsts.TEST_USER_NAME,
                       email=UsersConsts.TEST_USER_EMAIL,
                       password=UsersConsts.TEST_USER_PASSWORD,
                       permission_group_id=PermissionGroupsConsts.USER_GROUP_ID)

    return user


@pytest.fixture(scope="function")
def new_permission_group():
    group = models.PermissionGroup(name="test_group")

    return group


@pytest.fixture(scope="function")
def new_issue():
    issue = models.Issue(title="test_issue",
                         content="test content",
                         status=IssuesConsts.ISSUE_TODO,
                         owner_id=1,
                         project_id=1)

    return issue


@pytest.fixture(scope="function")
def new_project():
    project = models.Project(name="test_project",
                             owner_id=1)

    return project


@pytest.fixture(scope="session")
def test_client():
    flask_app = create_app(TestConfig)
    client = flask_app.test_client()

    with flask_app.test_request_context():
        user = models.User(username=UsersConsts.TEST_USER_NAME,
                           email=UsersConsts.TEST_USER_EMAIL,
                           password=UsersConsts.TEST_USER_PASSWORD,
                           permission_group_id=PermissionGroupsConsts.USER_GROUP_ID)

        user.password = account_utils.hash_password(user.password)

        db.session.add(user)
        db.session.commit()

        yield client


@pytest.fixture(scope="function")
def logged_test_admin(test_client):
    from flask_bug_tracker.app_modules import forms

    form = forms.LoginForm()
    form.email.data = os.environ.get("BUILD_IN_ADMIN_USERNAME")
    form.password.data = os.environ.get("BUILD_IN_ADMIN_PASSWORD")

    test_client.post(url_for("auth.login"), data=form.data, follow_redirects=True)

    yield

    test_client.get(url_for("auth.logout"), follow_redirects=True)


@pytest.fixture(scope="function")
def logged_test_user(test_client):
    from flask_bug_tracker.app_modules import forms

    form = forms.LoginForm()
    form.email.data = UsersConsts.TEST_USER_EMAIL
    form.password.data = UsersConsts.TEST_USER_PASSWORD

    test_client.post(url_for("auth.login"), data=form.data, follow_redirects=True)

    yield

    test_client.get(url_for("auth.logout"), follow_redirects=True)
