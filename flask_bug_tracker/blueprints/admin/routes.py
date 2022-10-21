from flask import Blueprint, render_template, flash, url_for, abort, redirect
import flask_login
from flask_bug_tracker.app_modules import decorators, forms
from flask_bug_tracker import models
from flask_bug_tracker.utils import db_utils, account_utils, table_utils
from flask_bug_tracker.consts import SystemMessagesConst, FlashConsts, PaginationConsts


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

    return render_template("navigation_page.html", page_options=admin_options)


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


@admin.route("/users", methods=["GET"], defaults={"page_id": 1})
@admin.route("/users/<int:page_id>", methods=["GET"])
@flask_login.login_required
@decorators.admin_required
def users_preview(page_id):
    users = models.User.query
    users = users.paginate(page=page_id, per_page=PaginationConsts.USERS_PER_PAGE)

    table_struct = table_utils.get_data_table_data_struct_for_users(users.items)

    return render_template("users.html", users=users, table_struct=table_struct)


@admin.route("/user/<user_id>", methods=["GET"])
@flask_login.login_required
@decorators.admin_required
def preview_user(user_id):
    user = models.User.query.filter_by(id=user_id).first()

    if user:
        update_user_form = forms.UpdateUserForm(user.id)

        update_user_form.username.data = user.username
        update_user_form.email.data = user.email
        update_user_form.permission_group.data = user.get_permission_group_name()

        return render_template("user.html", user=user, update_user_form=update_user_form)

    else:
        abort(404)


@admin.route("/users/<user_id>/update", methods=["POST"])
@flask_login.login_required
@decorators.admin_required
def update_user(user_id):
    user = models.User.query.filter_by(id=user_id).first()

    if user:
        update_user_form = forms.UpdateUserForm(user.id)

        if update_user_form.validate_on_submit():
            user.username = update_user_form.username.data
            user.email = update_user_form.email.data

            permission_group = update_user_form.permission_group.data
            permission_group_id = models.PermissionGroup.get_group_by_name(permission_group).id

            user.permission_group_id = permission_group_id

            db_utils.commit_session()

            flash(SystemMessagesConst.ACCOUNT_UPDATED, FlashConsts.FLASH_SUCCESS)

        else:
            flash(SystemMessagesConst.ERROR_WHILE_UPDATING_ACCOUNT, FlashConsts.FLASH_DANGER)

        return redirect(url_for("admin.preview_user", user_id=user.id))

    else:
        abort(404)


@admin.route("/users/<user_id>/remove", methods=["POST"])
@flask_login.login_required
@decorators.admin_required
def remove_user(user_id):
    user = models.User.query.filter_by(id=user_id).first()

    if user and user.id != flask_login.current_user.id:
        db_utils.remove_object_from_db(user)

        flash(SystemMessagesConst.ACCOUNT_REMOVED_SUCCESSFULLY, FlashConsts.FLASH_SUCCESS)

        return redirect(url_for("admin.users_preview", user_id=user.id))

    else:
        abort(404)
