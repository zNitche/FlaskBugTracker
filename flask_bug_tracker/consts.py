class SystemMessagesConst:
    LOGIN_ERROR = "Wrong email or/and password"
    EMAIL_TAKEN = "Email taken"
    USERNAME_TAKEN = "Username taken"
    PERMISSION_GROUP_DOESNT_EXIST = "Permission Group doesn't exist"
    ACCOUNT_CREATED = "Account {name} has been created"
    ACCOUNT_UPDATED = "Account has been updated successfully"
    ACCOUNT_REMOVED_SUCCESSFULLY = "Account has been removed successfully"
    ERROR_WHILE_UPDATING_ACCOUNT = "Error while updating account details"
    USER_DOESNT_EXIST = "User doesnt exist"
    ADDED_ISSUE = "Issue has been added successfully"
    ERROR_WHILE_ADDING_ISSUE = "Error while adding issue"


class FlashConsts:
    FLASH_DANGER = "danger"
    FLASH_INFO = "info"
    FLASH_SUCCESS = "success"


class PermissionGroupsConsts:
    USER_GROUP = "user"
    ADMIN_GROUP = "admin"

    USER_GROUP_ID = 1
    ADMIN_GROUP_ID = 2


class ValidationConsts:
    MIN_USERNAME_LENGTH = 2
    MAX_USERNAME_LENGTH = 20
    MIN_EMAIL_LENGTH = 2
    MAX_EMAIL_LENGTH = 50
    MIN_PASSWORD_LENGTH = 8
    MAX_PASSWORD_LENGTH = 20

    MIN_ISSUE_NAME_LENGTH = 2
    MAX_ISSUE_NAME_LENGTH = 20
    MIN_ISSUE_CONTENT_LENGTH = 10
    MAX_ISSUE_CONTENT_LENGTH = 200
