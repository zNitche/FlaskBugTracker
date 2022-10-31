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
    ISSUE_UPDATED = "Issue has been updated successfully"
    ISSUE_REMOVED_SUCCESSFULLY = "Issue has been removed successfully"
    ISSUE_WHILE_UPDATING_ACCOUNT = "Error while updating issue details"
    ERROR_WHILE_UPDATING_ISSUE = "Error while updating issue details"
    ISSUE_REMOVED = "Issue has been removed successfully"

    ISSUE_TITLE_TAKEN = "Issue title taken"
    PROJECT_NAME_TAKEN = "Project name taken"

    ADDED_PROJECT = "Project has been added successfully"
    ERROR_WHILE_ADDING_PROJECT = "Error while adding project"
    PROJECT_REMOVED = "Project has been removed"

    CANT_ACCESS_PROJECT = "Cant access project"


class FlashConsts:
    FLASH_DANGER = "danger"
    FLASH_INFO = "info"
    FLASH_SUCCESS = "success"


class PermissionGroupsConsts:
    USER_GROUP = "user"
    ADMIN_GROUP = "admin"

    USER_GROUP_ID = 1
    ADMIN_GROUP_ID = 2


class IssuesConsts:
    ISSUE_COMPLETED = "Completed"
    ISSUE_CANCELLED = "Cancelled"
    ISSUE_TODO = "ToDo"
    ISSUE_IN_PROGRESS = "In progress"

    ALL_ISSUES = "All"

    ISSUES_STATUS_TYPES = [ISSUE_TODO, ISSUE_IN_PROGRESS, ISSUE_COMPLETED, ISSUE_CANCELLED]
    ISSUES_STATUS_TYPES_FOR_FILTER = [ISSUE_TODO, ISSUE_IN_PROGRESS, ISSUE_COMPLETED, ISSUE_CANCELLED, ALL_ISSUES]


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
    MAX_ISSUE_CONTENT_LENGTH = 400

    MIN_PROJECT_NAME = 2
    MAX_PROJECT_NAME = 20

    MAX_USER_ACTION_LOG_LENGTH = 250


class PaginationConsts:
    USERS_PER_PAGE = 15
    ISSUES_PER_PAGE = 15
    LOGS_PER_HOME_PAGE = 20
    PROJECTS_PER_PAGE = 15


class UserActionsLogsConsts:
    ISSUE_ASSIGNED_TO_USER = "Issue #{issue_id} has been assigned to {assignee_name} by {reporter_name}"
    ISSUE_STATUS_CHANGED = "Issue #{issue_id} status changed to {issue_state} by {username}"
