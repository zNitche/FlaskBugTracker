def get_data_table_data_struct_for_users(users):
    headers = ["Username", "Email", "Permission Group", "Issues"]
    users_struct = {}

    for user in users:
        users_struct[user.id] = [
            user.username,
            user.email,
            user.get_permission_group_name(),
            len(user.issues)
        ]

    struct = {
            "headers": headers,
            "content": users_struct
        }

    return struct


def get_data_table_data_struct_for_issues(issues):
    headers = ["ID", "Title", "Owner", "Assigned to", "Date", "Last Update", "Status"]
    issues_struct = {}

    for issue in issues:
        issues_struct[issue.id] = [
            issue.id,
            issue.title,
            issue.get_owner_name(),
            issue.get_assigned_to_user_name(),
            issue.date,
            issue.last_updated,
            issue.status
        ]

    struct = {
            "headers": headers,
            "content": issues_struct
        }

    return struct


def get_data_table_data_struct_for_projects(projects):
    headers = ["ID", "Name", "Owner", "Date", "Members Count"]
    projects_struct = {}

    for project in projects:
        projects_struct[project.id] = [
            project.id,
            project.name,
            project.get_owner_name(),
            project.created_date,
            len(project.members)
        ]

    struct = {
            "headers": headers,
            "content": projects_struct
        }

    return struct
