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
