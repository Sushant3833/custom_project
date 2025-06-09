# Copyright (c) 2025, sushant and contributors
# For license information, please see license.txt

# import frappe

import frappe
from frappe.utils import getdate
from calendar import month_name

def execute(filters=None):
    columns = get_columns()
    data = []

    fiscal_year = frappe.get_doc("Fiscal Year", filters.get("fiscal_year"))
    fy_start = getdate(fiscal_year.year_start_date)
    fy_end = getdate(fiscal_year.year_end_date)

    projects = frappe.get_all("Project", 
        filters={"name": filters.project} if filters.project else {}, 
        fields=["name", "project_name", "custom_po_no","company"]
    )

    for project in projects:
        row = {
            "company":project.company,
            "project": project.name,
            "project_name": project.project_name,
            "po_number": project.custom_po_no,
            "total_po_cost": 0
        }

        # Initialize month values
        for m in range(1, 13):
            row[month_name[m]] = 0

        tasks = frappe.get_all("Task",
            filters={"project": project.name},
            fields=["custom_milestone_price", "exp_end_date"]
        )

        total = 0
        for task in tasks:
            price = task.custom_milestone_price or 0
            total += price
            if task.exp_end_date:
                date = getdate(task.exp_end_date)
                if fy_start <= date <= fy_end:
                    month = date.month
                    row[month_name[month]] += price

        row["total_po_cost"] = total
        data.append(row)

    return columns, data


def get_columns():
    columns = [
        {"label": "Company", "fieldname": "company", "fieldtype": "Link", "options": "Company", "width": 120},
        {"label": "Project", "fieldname": "project", "fieldtype": "Link", "options": "Project", "width": 120},
        {"label": "Project Name", "fieldname": "project_name", "fieldtype": "Data", "width": 150},
        {"label": "PO Number", "fieldname": "po_number", "fieldtype": "Data", "width": 120},
        {"label": "Total PO Cost", "fieldname": "total_po_cost", "fieldtype": "Currency", "width": 120}
    ]

    for m in range(1, 13):
        columns.append({
            "label": month_name[m],
            "fieldname": month_name[m],
            "fieldtype": "Currency",
            "width": 100
        })

    return columns

