import frappe
from frappe.utils import date_diff

def execute(filters=None):
    columns = [
        {"label": "Milestone", "fieldname": "milestone", "fieldtype": "Data", "width": 250},
        {"label": "Activity", "fieldname": "activity", "fieldtype": "Data", "width": 250},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 120},
        {"label": "Expected Start Date", "fieldname": "start_date", "fieldtype": "Date", "width": 120},
        {"label": "Expected End Date", "fieldname": "end_date", "fieldtype": "Date", "width": 180},
        {"label": "Actual Start Date", "fieldname": "completed_start_date", "fieldtype": "Date", "width": 180},
        {"label": "Actual End Date", "fieldname": "completed_end_date", "fieldtype": "Date", "width": 180},
        {"label": "Delayed in Days", "fieldname": "delayed_days", "fieldtype": "Int", "width": 180},
        {"label": "Delay Owner", "fieldname": "custom_delay_owner", "fieldtype": "Link","options":"User", "width": 180},
        {"label": "Notes", "fieldname": "custom_notes", "fieldtype": "Data", "width": 250},
    ]

    data = []

    # Get all milestone tasks
    # milestone_tasks = frappe.get_all("Task", filters={"is_milestone": 1}, fields=["name", "subject", "status", "exp_start_date", "exp_end_date", "completed_on",
    #                                                                               "custom_actual_start_date", "custom_actual_end_date", "custom_delay_owner", "custom_notes"])

    task_filters = {"is_milestone": 1}
    if filters and filters.get("project"):
        task_filters["project"] = filters.get("project")

    milestone_tasks = frappe.get_all("Task", filters=task_filters, fields=[
        "name", "subject", "status", "exp_start_date", "exp_end_date", "completed_on",
        "custom_actual_start_date", "custom_actual_end_date", "custom_delay_owner", "custom_notes"
    ])

    for parent_task in milestone_tasks:
        # Get all dependent tasks linked via depends_on child table
        dependents = frappe.get_all("Task Depends On", filters={"parent": parent_task.name}, fields=["task"])

        for dep in dependents:
            # Load dependent task full doc to get all fields
            child_task = frappe.get_doc("Task", dep.task)

            delayed_days = 0
            if child_task.exp_end_date and child_task.custom_actual_end_date:
                delayed_days = date_diff(child_task.custom_actual_end_date, child_task.exp_end_date)

            data.append({
                "":"",
                "milestone": "",
                "activity": child_task.subject,
                "status": child_task.status,
                "start_date": child_task.exp_start_date,
                "end_date": child_task.exp_end_date,
                "completed_start_date": child_task.custom_actual_start_date,
                "completed_end_date": child_task.custom_actual_end_date,
                "delayed_days": delayed_days if delayed_days > 0 else 0,
                "custom_delay_owner":child_task.custom_delay_owner,
                "custom_notes":child_task.custom_notes
            })

        # Also add the parent milestone task itself
        delayed_days_parent = 0
        if parent_task.exp_end_date and parent_task.custom_actual_end_date:
            delayed_days_parent = date_diff(parent_task.custom_actual_end_date, parent_task.exp_end_date)

        data.append({
            "milestone": parent_task.subject,
            "activity": parent_task.subject,
            "status": parent_task.status,
            "start_date": parent_task.exp_start_date,
            "end_date": parent_task.exp_end_date,
            "completed_start_date": parent_task.custom_actual_start_date,
            "completed_end_date": parent_task.custom_actual_end_date,
            "delayed_days": delayed_days_parent if delayed_days_parent > 0 else 0,
            "custom_delay_owner":parent_task.custom_delay_owner,
            "custom_notes":parent_task.custom_notes
        })

    return columns, data
