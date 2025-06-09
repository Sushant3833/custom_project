# Copyright (c) 2025, sushant and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
    filters = filters or {}

    conditions = ""
    if filters.get("project"):
        conditions += f" AND p.name = %(project)s"

    data = frappe.db.sql(f"""
        SELECT
            p.name AS project,
            p.project_name,
            p.custom_po_no,
            t.exp_end_date AS po_first_release_date,
            t.subject AS po_milestone,
            t.custom_milestone_price AS po_cost
        FROM `tabProject` p
        LEFT JOIN `tabTask` t ON t.project = p.name AND t.is_milestone = 1
        WHERE 1=1 {conditions}
        ORDER BY p.name
    """, filters, as_dict=True)

    columns = [
        {"label": "Project", "fieldname": "project", "fieldtype": "Link", "options": "Project", "width": 120},
        {"label": "Project Name", "fieldname": "project_name", "fieldtype": "Data", "width": 200},
        {"label": "PO Number", "fieldname": "custom_po_no", "fieldtype": "Data", "width": 120},
        {"label": "PO First Release Date", "fieldname": "po_first_release_date", "fieldtype": "Date", "width": 150},
        {"label": "PO Milestone", "fieldname": "po_milestone", "fieldtype": "Data", "width": 200},
        {"label": "PO Cost", "fieldname": "po_cost", "fieldtype": "Currency", "width": 120},
    ]

    return columns, data

