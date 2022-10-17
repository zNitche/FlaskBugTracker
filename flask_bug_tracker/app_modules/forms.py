from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from flask_bug_tracker.consts import ValidationConsts, SystemMessagesConst
from flask_bug_tracker import models


class FormBase(FlaskForm):
    def __init__(self):
        super().__init__()

        self.html_ignored_fields = ["CSRFTokenField"]


class LoginForm(FormBase):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])


class RegistrationForm(FormBase):
    username = StringField("Username", validators=[DataRequired(),
                                                   Length(min=ValidationConsts.MIN_USERNAME_LENGTH,
                                                          max=ValidationConsts.MAX_USERNAME_LENGTH)])

    email = StringField("Email", validators=[DataRequired(),
                                             Length(min=ValidationConsts.MIN_EMAIL_LENGTH,
                                                    max=ValidationConsts.MAX_EMAIL_LENGTH)])

    password = PasswordField("Password", validators=[DataRequired(),
                                                     Length(min=ValidationConsts.MIN_PASSWORD_LENGTH,
                                                            max=ValidationConsts.MAX_PASSWORD_LENGTH)])

    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])

    permission_group = SelectField("Permission Group", choices=models.PermissionGroup.get_groups_names())

    def validate_username(self, username):
        user = models.User.query.filter_by(username=username.data).first()

        if user:
            raise ValidationError(SystemMessagesConst.USERNAME_TAKEN)

    def validate_email(self, email):
        user = models.User.query.filter_by(email=email.data).first()

        if user:
            raise ValidationError(SystemMessagesConst.EMAIL_TAKEN)

    def validate_permission_group(self, permission_group):
        permission_group = models.PermissionGroup.query.filter_by(name=permission_group.data).first()

        if not permission_group:
            raise ValidationError(SystemMessagesConst.PERMISSION_GROUP_DOESNT_EXIST)
