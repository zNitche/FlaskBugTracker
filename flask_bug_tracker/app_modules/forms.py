from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Optional
from flask_bug_tracker.consts import ValidationConsts, SystemMessagesConst
from flask_bug_tracker import models


class FormBase(FlaskForm):
    def __init__(self):
        super().__init__()

        self.html_ignored_fields = ["CSRFTokenField"]


class UserValidationMixin:
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


class LoginForm(FormBase):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])


class RegistrationForm(FormBase, UserValidationMixin):
    username = StringField("Username", validators=[DataRequired(),
                                                   Length(min=ValidationConsts.MIN_USERNAME_LENGTH,
                                                          max=ValidationConsts.MAX_USERNAME_LENGTH)])

    email = StringField("Email", validators=[DataRequired(),
                                             Length(min=ValidationConsts.MIN_EMAIL_LENGTH,
                                                    max=ValidationConsts.MAX_EMAIL_LENGTH)])

    password = PasswordField("Password (optional)", validators=[Optional(),
                                                                Length(min=ValidationConsts.MIN_PASSWORD_LENGTH,
                                                                       max=ValidationConsts.MAX_PASSWORD_LENGTH)])

    confirm_password = PasswordField("Confirm Password (optional)", validators=[EqualTo("password")])

    permission_group = SelectField("Permission Group", choices=models.PermissionGroup.get_groups_names())


class UpdateUserForm(FormBase, UserValidationMixin):
    def __init__(self, current_user_id):
        super().__init__()

        self.current_user_id = current_user_id

    username = StringField("Username", validators=[DataRequired(),
                                                   Length(min=ValidationConsts.MIN_USERNAME_LENGTH,
                                                          max=ValidationConsts.MAX_USERNAME_LENGTH)])

    email = StringField("Email", validators=[DataRequired(),
                                             Length(min=ValidationConsts.MIN_EMAIL_LENGTH,
                                                    max=ValidationConsts.MAX_EMAIL_LENGTH)])

    permission_group = SelectField("Permission Group", choices=models.PermissionGroup.get_groups_names())

    def validate_username(self, username):
        user = models.User.query.filter_by(username=username.data).first()

        if user and (user.id != self.current_user_id):
            raise ValidationError(SystemMessagesConst.USERNAME_TAKEN)

    def validate_email(self, email):
        user = models.User.query.filter_by(email=email.data).first()

        if user and (user.id != self.current_user_id):
            raise ValidationError(SystemMessagesConst.EMAIL_TAKEN)


class AddIssueForm(FormBase):
    title = StringField("Title", validators=[DataRequired(),
                                             Length(min=ValidationConsts.MIN_ISSUE_NAME_LENGTH,
                                                    max=ValidationConsts.MAX_ISSUE_NAME_LENGTH)])

    content = TextAreaField("Content", validators=[DataRequired(),
                                                   Length(min=ValidationConsts.MIN_ISSUE_CONTENT_LENGTH,
                                                          max=ValidationConsts.MAX_ISSUE_CONTENT_LENGTH)])

    assigned_to_user_name = SelectField("Assign To", choices=[])

    def validate_assigned_to_user_name(self, assigned_to_user_name):
        user = models.User.query.filter_by(username=assigned_to_user_name.data).first()

        if not user:
            raise ValidationError(SystemMessagesConst.USER_DOESNT_EXIST)
