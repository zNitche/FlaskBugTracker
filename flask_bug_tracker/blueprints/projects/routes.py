from flask import Blueprint, render_template, url_for
import flask_login


projects = Blueprint("projects", __name__, template_folder="templates", static_folder="static", url_prefix="/projects")


@projects.route("/")
@flask_login.login_required
def home():
    page_options = [
        {
            "content": "Add Project",
            "url": "#"
        },
        {
            "content": "My Projects",
            "url": "#"
        },
    ]

    if flask_login.current_user.is_admin():
        page_options.append({
            "content": "All Projects",
            "url": "#"
        })

    return render_template("navigation_page.html", page_options=page_options)
