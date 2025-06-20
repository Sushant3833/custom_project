# Copyright (c) 2025, sushant and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import flt
from datetime import datetime, timedelta

def execute(filters=None):
    filters = filters or {}

    # Date Calculations
    now = datetime.now()
    current_month = now.month
    current_month_name = now.strftime("%B")
    next_month = (now + timedelta(days=32)).month
    next_month_name = (now + timedelta(days=32)).strftime("%B")
    next_to_next_month = (now + timedelta(days=64)).month
    next_to_next_month_name = (now + timedelta(days=64)).strftime("%B")

    # Apply filters
    conditions = ""
    if filters.get("project"):
        conditions += f" AND p.name = %(project)s"

    # Fetch project and task data
    data = frappe.db.sql(f"""
        SELECT
            p.name AS project,
            p.project_name,
            p.custom_po_no,
            t.name AS task_name,
            t.exp_end_date AS po_first_release_date,
            t.subject AS po_milestone,
            t.custom_milestone_price AS po_cost,
            MONTH(t.exp_end_date) AS exp_month
        FROM `tabProject` p
        LEFT JOIN `tabTask` t ON t.project = p.name AND t.is_milestone = 1
        WHERE 1=1 {conditions}
        ORDER BY p.name
    """, filters, as_dict=True)

    for row in data:
        row["bill_done_till_month"] = 0
        row["collection"] = 0
        row["billing_expected_next_month"] = 0
        row["billing_expected_next_to_next_month"] = 0

        if row.get("project") and row.get("task_name"):
            # Actual billed amount from Sales Invoice in current month
            billed_amount = frappe.db.sql("""
                SELECT SUM(grand_total)
                FROM `tabSales Invoice`
                WHERE docstatus = 1
                  AND project = %s
                  AND custom_task = %s
                  AND MONTH(posting_date) = %s
            """, (row["project"], row["task_name"], current_month))
            row["bill_done_till_month"] = billed_amount[0][0] if billed_amount and billed_amount[0][0] else 0

            # Actual collection from Payment Entry
            collection = frappe.db.sql("""
                SELECT SUM(pe.paid_amount)
                FROM `tabPayment Entry` pe
                JOIN `tabPayment Entry Reference` per ON per.parent = pe.name
                JOIN `tabSales Invoice` si ON per.reference_name = si.name
                WHERE
                    pe.docstatus = 1
                    AND per.reference_doctype = 'Sales Invoice'
                    AND si.project = %s
                    AND si.custom_task = %s
            """, (row["project"], row["task_name"]))
            row["collection"] = collection[0][0] if collection and collection[0][0] else 0

        # Expected billing based on milestone month
        if row.get("exp_month") == next_month:
            row["billing_expected_next_month"] = row.get("po_cost", 0)
        if row.get("exp_month") == next_to_next_month:
            row["billing_expected_next_to_next_month"] = row.get("po_cost", 0)

    columns = [
        {"label": "Project", "fieldname": "project", "fieldtype": "Link", "options": "Project", "width": 120},
        {"label": "Project Name", "fieldname": "project_name", "fieldtype": "Data", "width": 200},
        {"label": "PO Number", "fieldname": "custom_po_no", "fieldtype": "Data", "width": 120},
        {"label": "PO First Release Date", "fieldname": "po_first_release_date", "fieldtype": "Date", "width": 150},
        {"label": "PO Milestone", "fieldname": "po_milestone", "fieldtype": "Data", "width": 200},
        {"label": "PO Cost", "fieldname": "po_cost", "fieldtype": "Currency", "width": 120},
        {"label": f"Bill Done Till ({current_month_name})", "fieldname": "bill_done_till_month", "fieldtype": "Currency", "width": 160},
        {"label": "Collection", "fieldname": "collection", "fieldtype": "Currency", "width": 120},
        {"label": f"Billing Expected In ({next_month_name})", "fieldname": "billing_expected_next_month", "fieldtype": "Currency", "width": 180},
        {"label": f"Billing Expected In ({next_to_next_month_name})", "fieldname": "billing_expected_next_to_next_month", "fieldtype": "Currency", "width": 200},
    ]

    return columns, data
