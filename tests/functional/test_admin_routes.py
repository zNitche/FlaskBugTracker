from flask import url_for
import flask_login
from flask_bug_tracker import models
from flask_bug_tracker.consts import PermissionGroupsConsts


def test_admin_page_as_user(test_client, logged_test_user):
    assert not flask_login.current_user.is_admin()

    response = test_client.get(url_for("admin.home"), follow_redirects=True)

    assert response.status_code == 403


def test_admin_page_as_admin(test_client, logged_test_admin):
    response = test_client.get(url_for("admin.home"), follow_redirects=True)

    assert response.status_code == 200
    assert response.request.path == url_for("admin.home")


def test_register_account(test_client, logged_test_admin):
    from flask_bug_tracker.app_modules import forms

    response = test_client.get(url_for("admin.register_account"), follow_redirects=True)
    assert response.status_code == 200

    registration_form = forms.RegistrationForm()

    registration_form.username.data = "test_user_2"
    registration_form.email.data = "test_user_2@email.com"
    registration_form.password.data = "test_pass_2"
    registration_form.confirm_password.data = "test_pass_2"
    registration_form.permission_group.data = models.PermissionGroup.query.filter_by(
        id=PermissionGroupsConsts.USER_GROUP_ID).first().name

    response = test_client.post(url_for("admin.register_account"), data=registration_form.data, follow_redirects=True)

    assert response.status_code == 200

    new_user = models.User.query.filter_by(email="test_user_2@email.com").first()

    assert new_user
