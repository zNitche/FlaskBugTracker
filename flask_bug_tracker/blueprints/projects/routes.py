from flask import Blueprint, render_template, url_for, flash, request, redirect, abort
import flask_login
from flask_bug_tracker import models
from flask_bug_tracker.consts import PaginationConsts, SystemMessagesConst, FlashConsts
from flask_bug_tracker.utils import table_utils, db_utils, projects_utils
from flask_bug_tracker.app_modules import forms, decorators


projects = Blueprint("projects", __name__, template_folder="templates", static_folder="static", url_prefix="/projects")


@projects.route("/")
@flask_login.login_required
def home():
    page_options = [
        {
            "content": "Add Project",
            "url": url_for('projects.add_project')
        },
        {
            "content": "My Projects",
            "url": url_for('projects.preview_my_projects')
        },
    ]

    if flask_login.current_user.is_admin():
        page_options.append({
            "content": "All Projects",
            "url": url_for('projects.preview_all_projects')
        })

    return render_template("navigation_page.html", page_options=page_options)


@projects.route("/all", defaults={"page_id": 1}, methods=["GET", "POST"])
@projects.route("/all/<int:page_id>", methods=["GET", "POST"])
@flask_login.login_required
@decorators.admin_required
def preview_all_projects(page_id):
    projects = models.Project.query.order_by(models.Project.created_date.desc())
    projects = projects.paginate(page=page_id, per_page=PaginationConsts.PROJECTS_PER_PAGE)

    table_struct = table_utils.get_data_table_data_struct_for_projects(projects.items)

    return render_template("preview_projects.html", projects=projects, table_struct=table_struct)


@projects.route("/my", defaults={"page_id": 1}, methods=["GET", "POST"])
@projects.route("/my/<int:page_id>", methods=["GET", "POST"])
@flask_login.login_required
def preview_my_projects(page_id):
    current_user = flask_login.current_user

    projects = models.Project.query.order_by(models.Project.created_date.desc()).filter(
        (models.Project.owner_id == current_user.id) | (models.Project.members.any(models.User.id == current_user.id)))

    projects = projects.paginate(page=page_id, per_page=PaginationConsts.PROJECTS_PER_PAGE)

    table_struct = table_utils.get_data_table_data_struct_for_projects(projects.items)

    return render_template("preview_projects.html", projects=projects, table_struct=table_struct)


@projects.route("/add", methods=["GET", "POST"])
@flask_login.login_required
def add_project():
    add_project_form = forms.AddProjectForm()
    user = flask_login.current_user

    if add_project_form.validate_on_submit():
        name = add_project_form.name.data

        project = models.Project(name=name, owner_id=user.id)

        db_utils.add_object_to_db(project)

        flash(SystemMessagesConst.ADDED_PROJECT, FlashConsts.FLASH_SUCCESS)

    elif not add_project_form.validate_on_submit() and request.method == "POST":
        flash(SystemMessagesConst.ERROR_WHILE_ADDING_PROJECT, FlashConsts.FLASH_DANGER)

    if request.method == "POST":
        return redirect(url_for("projects.preview_my_projects"))

    return render_template("add_project.html", add_project_form=add_project_form)


@projects.route("/project/<project_name>", methods=["GET"])
@flask_login.login_required
def preview_project(project_name):
    project = models.Project.query.filter_by(name=project_name).first()

    if project and (projects_utils.check_project_access(project, flask_login.current_user) or
                    flask_login.current_user in project.members):

        return render_template("project.html", project=project)

    else:
        abort(404)


@projects.route("/project/<project_name>/remove", methods=["POST"])
@flask_login.login_required
def remove_project(project_name):
    project = models.Project.query.filter_by(name=project_name).first()

    if project and projects_utils.check_project_access(project, flask_login.current_user):
        db_utils.remove_object_from_db(project)

        flash(SystemMessagesConst.PROJECT_REMOVED, FlashConsts.FLASH_SUCCESS)

        return redirect(url_for("projects.preview_my_projects"))

    else:
        abort(404)


@projects.route("/project/<project_name>/add_member", methods=["GET", "POST"])
@flask_login.login_required
def add_project_member(project_name):
    project = models.Project.query.filter_by(name=project_name).first()

    if project and projects_utils.check_project_access(project, flask_login.current_user):
        add_project_member_form = forms.AddProjectMember()

        if request.method == "POST":
            if add_project_member_form.validate_on_submit():
                email = add_project_member_form.email.data
                new_member = models.User.query.filter_by(email=email).first()

                if new_member not in project.members and new_member.id != project.owner_id:
                    project.members.append(new_member)

                    db_utils.commit_session()

                    flash(SystemMessagesConst.ADDED_PROJECT_MEMBER, FlashConsts.FLASH_SUCCESS)

                    return redirect(url_for("projects.preview_project", project_name=project_name))

                else:
                    flash(SystemMessagesConst.USER_IS_ALREADY_PROJECT_MEMBER, FlashConsts.FLASH_DANGER)

            else:
                flash(SystemMessagesConst.ERROR_WHILE_ADDING_PROJECT_MEMBER, FlashConsts.FLASH_DANGER)

        return render_template("add_project_member.html", project=project,
                               add_project_member_form=add_project_member_form)

    else:
        abort(404)


@projects.route("/project/<project_name>/remove_member/<member_email>", methods=["POST"])
@flask_login.login_required
def remove_project_member(project_name, member_email):
    project = models.Project.query.filter_by(name=project_name).first()
    member = models.User.query.filter_by(email=member_email).first()

    if project and projects_utils.check_project_access(project, flask_login.current_user) and member:
        if member in project.members:
            project.members.remove(member)

            db_utils.commit_session()

            flash(SystemMessagesConst.REMOVED_PROJECT_MEMBER, FlashConsts.FLASH_SUCCESS)

        else:
            flash(SystemMessagesConst.ERROR_WHILE_REMOVING_PROJECT_MEMBER, FlashConsts.FLASH_DANGER)

        return redirect(url_for("projects.preview_project", project_name=project_name))

    else:
        abort(404)
