from flask_bug_tracker import models


def check_project_access(project, user):
    status = False

    if (project.owner_id == user.id) or user.is_admin():
        status = True

    return status


def get_projects_for_user(user):
    projects = []

    for project in user.projects:
        projects.append(project)

    owned_projects = models.Project.query.filter_by(owner_id=user.id).all()

    for project in owned_projects:
        projects.append(project)

    return projects
