from flask import Blueprint, render_template
import flask_login


admin = Blueprint("admin", __name__, template_folder="templates", static_folder="static", url_prefix="/admin")


@admin.route("/")
@flask_login.login_required
def home():
    return render_template("admin.html")
