from flask import Blueprint, render_template, flash
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
    return render_template("admin.html")


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

        password_hash = account_utils.hash_password(password)
        permission_group_id = models.PermissionGroup.get_group_by_name(permission_group).id

        user = models.User(username=username, email=email, password=password_hash,
                           permission_group_id=permission_group_id)

        db_utils.add_object_to_db(user)

        flash(SystemMessagesConst.ACCOUNT_CREATED.format(name=username), FlashConsts.FLASH_INFO)

    return render_template("register_account.html", registration_form=registration_form)
