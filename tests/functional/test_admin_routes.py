from flask import url_for
import flask_login


def test_admin_page_as_user(test_client, logged_test_user):
    assert not flask_login.current_user.is_admin()

    response = test_client.get(url_for("admin.home"), follow_redirects=True)

    assert response.status_code == 403


def test_admin_page_as_admin(test_client, logged_test_admin):
    response = test_client.get(url_for("admin.home"), follow_redirects=True)

    assert response.status_code == 200
    assert response.request.path == url_for("admin.home")
