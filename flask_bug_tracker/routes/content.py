from flask import Blueprint, render_template
import flask_login


content = Blueprint("content", __name__, template_folder="templates", static_folder="static", url_prefix="/")


@content.route("/")
@flask_login.login_required
def home():
    return render_template("content/index.html")
