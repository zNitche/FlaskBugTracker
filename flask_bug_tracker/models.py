from flask_bug_tracker import db
from flask_login import UserMixin
from datetime import datetime
from flask_bug_tracker.consts import PermissionGroupsConsts, ValidationConsts, IssuesConsts


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(ValidationConsts.MAX_USERNAME_LENGTH), unique=True, nullable=False)
    email = db.Column(db.String(ValidationConsts.MAX_EMAIL_LENGTH), unique=True, nullable=True)
    password = db.Column(db.String(128), unique=False, nullable=False)

    permission_group_id = db.Column(db.Integer, db.ForeignKey("permission_groups.id"), nullable=False)

    issues = db.relationship("Issue", backref="user", lazy=True)

    def get_permission_group_name(self):
        group = PermissionGroup.query.filter_by(id=self.permission_group_id).first()

        return group.name

    def is_admin(self):
        status = True if self.get_permission_group_name() == PermissionGroupsConsts.ADMIN_GROUP else False

        return status


class PermissionGroup(db.Model):
    __tablename__ = "permission_groups"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    users = db.relationship("User", backref="permission_group", lazy=True)

    @staticmethod
    def get_groups_names():
        groups = PermissionGroup.query.all()

        names = [group.name for group in groups]

        return names

    @staticmethod
    def get_group_by_name(name):
        groups = PermissionGroup.query.all()
        group = None

        for g in groups:
            if g.name == name:
                group = g

                break

        return group


class Issue(db.Model):
    __tablename__ = "issues"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(ValidationConsts.MAX_ISSUE_NAME_LENGTH), unique=True, nullable=False)
    content = db.Column(db.String(ValidationConsts.MAX_ISSUE_CONTENT_LENGTH), unique=False, nullable=True)

    status = db.Column(db.String(30), unique=False, nullable=False, default=IssuesConsts.ISSUE_TODO)

    date = db.Column(db.DateTime, unique=False, nullable=False, default=datetime.utcnow)
    last_updated = db.Column(db.DateTime, unique=False, nullable=True, default=datetime.utcnow)

    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    assigned_to_user_id = db.Column(db.Integer, unique=False, nullable=True, default=None)

    def get_owner_name(self):
        user = User.query.filter_by(id=self.owner_id).first()

        return user.username

    def get_assigned_to_user_name(self):
        user = User.query.filter_by(id=self.assigned_to_user_id).first()

        return user.username if user else ""


class UserActionLog(db.Model):
    __tablename__ = "user_action_logs"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=False, nullable=False)
    another_user_id = db.Column(db.Integer, unique=False, nullable=True)
    content = db.Column(db.String(ValidationConsts.MAX_USER_ACTION_LOG_LENGTH), unique=False, nullable=True)

    date = db.Column(db.DateTime, unique=False, nullable=False, default=datetime.utcnow)

    @staticmethod
    def get_actions_for_user_id(user_id):
        logs = UserActionLog.query.filter(
            (UserActionLog.user_id == user_id) | (UserActionLog.another_user_id == user_id)
        ).order_by(UserActionLog.date.desc()).all()

        return logs

