from flask import Blueprint, render_template
import flask_login


content = Blueprint("content", __name__, template_folder="template", static_folder="static")


@content.route("/")
@flask_login.login_required
def home():
    return render_template("index.html")
