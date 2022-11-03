from flask_bug_tracker.consts import PermissionGroupsConsts, IssuesConsts


def test_new_admin_user(new_admin_user):
    assert new_admin_user.username == "test_admin_user"
    assert new_admin_user.email == "test_admin_user@email.com"
    assert new_admin_user.password == "test_password"
    assert new_admin_user.permission_group_id == PermissionGroupsConsts.ADMIN_GROUP_ID


def test_new_regular_user(new_regular_user):
    assert new_regular_user.username == "test_user"
    assert new_regular_user.email == "test_user@email.com"
    assert new_regular_user.password == "test_password"
    assert new_regular_user.permission_group_id == PermissionGroupsConsts.USER_GROUP_ID


def test_new_permission_group(new_permission_group):
    assert new_permission_group.name == "test_group"


def test_new_issue(new_issue):
    assert new_issue.title == "test_issue"
    assert new_issue.content == "test content"
    assert new_issue.status == IssuesConsts.ISSUE_TODO
    assert new_issue.owner_id == 1
    assert new_issue.project_id == 1


def test_new_project(new_project):
    assert new_project.name == "test_project"
    assert new_project.owner_id == 1
