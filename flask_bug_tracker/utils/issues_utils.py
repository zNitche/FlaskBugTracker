def check_issue_access(issue, user):
    status = False

    if (issue.owner_id == user.id) or user.is_admin():
        status = True

    return status
