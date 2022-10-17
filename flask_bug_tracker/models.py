from flask_bug_tracker import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=True)
    password = db.Column(db.String(128), nullable=False)

    permission_group_id = db.Column(db.Integer, db.ForeignKey("permission_groups.id"), nullable=False)

    def get_permission_group_name(self):
        group = PermissionGroup.query.filter_by(id=self.permission_group_id).first()

        return group.name


class PermissionGroup(db.Model):
    __tablename__ = "permission_groups"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    users = db.relationship("User", backref="permission_group", lazy=True)

