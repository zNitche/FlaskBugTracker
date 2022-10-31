def check_project_access(project, user):
    status = False

    if (project.owner_id == user.id) or user.is_admin():
        status = True

    return status
