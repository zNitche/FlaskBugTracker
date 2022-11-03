from flask import Blueprint, abort, send_file
import flask_login
from flask_bug_tracker import models
from flask_bug_tracker.utils import reports_utils
from datetime import datetime


download = Blueprint("download", __name__, template_folder="templates", static_folder="static", url_prefix="/download")


@download.route("/project/<project_name>/report", methods=["GET"])
@flask_login.login_required
def download_project_report(project_name):
    project = models.Project.query.filter_by(name=project_name).first()
    user = flask_login.current_user

    if project and user in project.members or user.id == project.owner_id:
        report_struct = reports_utils.generate_project_report(project)

        with reports_utils.tmp_file() as file:
            file_path = reports_utils.get_tmp_file_path(file)
            reports_utils.save_report_to_csv(file_path, report_struct)

            return send_file(file_path, as_attachment=True,
                             download_name=f"{project_name}_{datetime.timestamp(datetime.now())}.csv")

    abort(404)
