from werkzeug.security import generate_password_hash, check_password_hash
from flask_bug_tracker import models
from flask_bug_tracker.consts import PermissionGroupsConsts
from flask_bug_tracker.utils import db_utils


def hash_password(password):
    return generate_password_hash(password)


def compare_password_with_hash(password, password_hash):
    return check_password_hash(password_hash, password)


def init_buildin_account(username, password):
    if len(models.User.query.all()) == 0:
        password = hash_password(password)

        admin = models.User(username=username, email=username, password=password,
                            permission_group_id=PermissionGroupsConsts.ADMIN_GROUP_ID)

        db_utils.add_object_to_db(admin)


def init_buildin_permissions_groups():
    if len(models.PermissionGroup.query.all()) == 0:
        user_group = models.PermissionGroup(name=PermissionGroupsConsts.USER_GROUP)
        admin_group = models.PermissionGroup(name=PermissionGroupsConsts.ADMIN_GROUP)

        db_utils.add_object_to_db(user_group)
        db_utils.add_object_to_db(admin_group)
