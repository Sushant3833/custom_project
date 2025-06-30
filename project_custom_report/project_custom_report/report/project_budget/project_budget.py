# Copyright (c) 2025
# For license information, please see license.txt

import frappe

def execute(filters=None):
    if not filters:
        filters = {}

    # Define columns
    columns = [
        {"label": "CRM ID", "fieldname": "crm_id", "fieldtype": "Data", "width": 120},
        {"label": "Project ID", "fieldname": "project_id", "fieldtype": "Data", "width": 120},
        {"label": "Project Name", "fieldname": "project_name", "fieldtype": "Data", "width": 200},
        {"label": "State/City", "fieldname": "state_city", "fieldtype": "Data", "width": 120},
        {"label": "PO Number", "fieldname": "po_number", "fieldtype": "Data", "width": 120},
        {"label": "Admin Cost", "fieldname": "admin_cost", "fieldtype": "Currency", "width": 120},
        {"label": "Internal Resource Cost", "fieldname": "internal_cost", "fieldtype": "Currency", "width": 150},
        {"label": "Service Cost", "fieldname": "service_cost", "fieldtype": "Currency", "width": 120},
        {"label": "Material Cost", "fieldname": "material_cost", "fieldtype": "Currency", "width": 120},
        {"label": "Total", "fieldname": "total_cost", "fieldtype": "Currency", "width": 120},
    ]

    # Fetch project data
    conditions = ""
    if filters.get("project"):
        conditions = f"where name = {frappe.db.escape(filters['project'])}"

    projects = frappe.db.sql(f"""
        SELECT
            name,
            custom_crm_id,
            custom_project_id,
            project_name,
            custom_statecity,
            custom_po_no,
            custom_total_expense_travel,
            custom_total_expense_food,
            custom_total_expense_stay,
            custom_total_internal_costing,
            custom_total_expense_service,
            custom_total_expense_supply
        FROM `tabProject`
        {conditions}
        ORDER BY creation DESC
    """, as_dict=True)

    data = []

    for p in projects:
        admin_cost = (p.custom_total_expense_travel or 0) + (p.custom_total_expense_food or 0) + (p.custom_total_expense_stay or 0)
        internal_cost = p.custom_total_internal_costing or 0
        service_cost = p.custom_total_expense_service or 0
        material_cost = p.custom_total_expense_supply or 0
        total = admin_cost + internal_cost + service_cost + material_cost

        data.append({
            "crm_id": p.custom_crm_id,
            "project_id": p.custom_project_id,
            "project_name": p.project_name,
            "state_city": p.custom_statecity,
            "po_number": p.custom_po_no,
            "admin_cost": admin_cost,
            "internal_cost": internal_cost,
            "service_cost": service_cost,
            "material_cost": material_cost,
            "total_cost": total
        })

    return columns, data
