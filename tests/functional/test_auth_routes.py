from flask import url_for
import os


def test_login(test_client):
    from flask_bug_tracker.app_modules import forms

    form = forms.LoginForm()
    form.email.data = os.environ.get("BUILD_IN_ADMIN_USERNAME")
    form.password.data = os.environ.get("BUILD_IN_ADMIN_PASSWORD")

    response = test_client.post(url_for("auth.login"), data=form.data, follow_redirects=True)

    assert response.status_code == 200
    assert response.request.path == url_for("main_app.home")


def test_logout(logged_test_user):
    response = logged_test_user.get(url_for("auth.logout"), follow_redirects=True)

    assert response.status_code == 200
    assert response.request.path == url_for("auth.login")

    response = logged_test_user.get(url_for("main_app.home"), follow_redirects=True)

    assert response.status_code == 200
    assert response.request.path == url_for("auth.login")
