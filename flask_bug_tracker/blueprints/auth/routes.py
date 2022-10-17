from flask import Blueprint, render_template, redirect, url_for, flash
import flask_login
from flask_bug_tracker.app_modules import forms
from flask_bug_tracker import models
from flask_bug_tracker.utils import account_utils
from flask_bug_tracker.consts import SystemMessagesConst, FlashConsts


auth = Blueprint("auth", __name__, template_folder="templates", static_folder="static", url_prefix="/auth")


@auth.route("/login", methods=["GET", "POST"])
def login():
    if flask_login.current_user.is_authenticated:
        return redirect(url_for("main_app.home"))

    login_form = forms.LoginForm()

    if login_form.validate_on_submit():
        user = models.User.query.filter_by(email=login_form.email.data).first()

        if user and account_utils.check_password_hash(user.password, login_form.password.data):
            flask_login.login_user(user)

            return redirect(url_for("main_app.home"))

        else:
            flash(SystemMessagesConst.LOGIN_ERROR, FlashConsts.FLASH_DANGER)

    return render_template("login.html", login_form=login_form)


@auth.route("/logout")
@flask_login.login_required
def logout():
    flask_login.logout_user()

    return redirect(url_for("main_app.home"))
