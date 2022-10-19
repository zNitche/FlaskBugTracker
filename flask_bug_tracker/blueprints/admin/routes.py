from flask import Blueprint, render_template, flash, url_for
import flask_login
from flask_bug_tracker.app_modules import decorators, forms
from flask_bug_tracker import models
from flask_bug_tracker.utils import db_utils, account_utils
from flask_bug_tracker.consts import SystemMessagesConst, FlashConsts


admin = Blueprint("admin", __name__, template_folder="templates", static_folder="static", url_prefix="/admin")


@admin.route("/")
@flask_login.login_required
@decorators.admin_required
def home():
    admin_options = [
        {
            "content": "Accounts Registration",
            "url": url_for('admin.register_account')
        },
        {
            "content": "Users Management",
            "url": url_for('admin.users_preview')
        }
    ]

    return render_template("admin.html", admin_options=admin_options)


@admin.route("/register_account", methods=["GET", "POST"])
@flask_login.login_required
@decorators.admin_required
def register_account():
    registration_form = forms.RegistrationForm()

    if registration_form.validate_on_submit():
        username = registration_form.username.data
        email = registration_form.email.data
        password = registration_form.password.data
        permission_group = registration_form.permission_group.data

        password = password if password is not "" else account_utils.generate_random_password()

        password_hash = account_utils.hash_password(password)
        permission_group_id = models.PermissionGroup.get_group_by_name(permission_group).id

        user = models.User(username=username, email=email, password=password_hash,
                           permission_group_id=permission_group_id)

        db_utils.add_object_to_db(user)

        flash(SystemMessagesConst.ACCOUNT_CREATED.format(name=username), FlashConsts.FLASH_SUCCESS)

    return render_template("register_account.html", registration_form=registration_form)


@admin.route("/users", methods=["GET"])
@flask_login.login_required
@decorators.admin_required
def users_preview():
    users = models.User.query.all()

    return render_template("users.html", users=users)
