from flask import Blueprint, render_template, redirect, url_for


errors = Blueprint("errors", __name__, template_folder='template', static_folder='static')


@errors.app_errorhandler(404)
def error_404(error):
    return render_template("error.html", error=error)


@errors.app_errorhandler(500)
def error_500(error):
    return render_template("error.html", error=error)


@errors.app_errorhandler(405)
def error_405(error):
    return render_template("error.html", error=error)


@errors.app_errorhandler(401)
def error_401(error):
    return redirect(url_for("auth.login"))

