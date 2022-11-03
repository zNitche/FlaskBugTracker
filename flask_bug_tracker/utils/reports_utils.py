import tempfile
from contextlib import contextmanager
import os
import csv


def generate_project_report(project):
    issues_struct = []

    for issue in project.issues:
        issue_struct = {
            "ID": issue.id,
            "Title": issue.title,
            "Project": issue.project.name,
            "Assigned to": issue.get_assigned_to_user_name(),
            "Date": issue.date,
            "Last Update": issue.last_updated,
            "Status": issue.status
        }

        issues_struct.append(issue_struct)

    struct = {
        "headers": [key for key in issues_struct[0].keys()] if len(issues_struct) > 0 else [],
        "content": issues_struct
    }

    return struct


def save_report_to_csv(file_path, report_struct):
    with open(file_path, mode="a") as csv_file:
        headers = report_struct["headers"]
        content = report_struct["content"]

        writer = csv.DictWriter(csv_file, fieldnames=headers)

        writer.writeheader()

        for data_row in content:
            writer.writerow(data_row)


def get_tmp_file_path(tmp_file):
    path = os.path.join(tempfile.gettempdir(), tmp_file.name)

    return path


@contextmanager
def tmp_file():
    tmp = tempfile.NamedTemporaryFile(delete=True)

    try:
        yield tmp

    finally:
        tmp.close()
