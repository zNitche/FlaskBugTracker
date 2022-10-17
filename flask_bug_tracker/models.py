from flask_bug_tracker import db
from flask_login import UserMixin
from flask_bug_tracker.consts import PermissionGroupsConsts, ValidationConsts


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(ValidationConsts.MAX_USERNAME_LENGTH), unique=True, nullable=False)
    email = db.Column(db.String(ValidationConsts.MAX_EMAIL_LENGTH), unique=True, nullable=True)
    password = db.Column(db.String(128), unique=False, nullable=False)

    permission_group_id = db.Column(db.Integer, db.ForeignKey("permission_groups.id"), nullable=False)

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
