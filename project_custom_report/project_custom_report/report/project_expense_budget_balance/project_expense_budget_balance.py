# Copyright (c) 2025, sushant and contributors
# For license information, please see license.txt

import frappe



def execute(filters=None):
    filters = filters or {}

    columns = [
        {"label": "Project", "fieldname": "name", "fieldtype": "Link", "options": "Project", "width": 150},
        {"label": "Project Name", "fieldname": "project_name", "fieldtype": "Data", "width": 200},

        {"label": "Travel Expense", "fieldname": "travel_expense", "fieldtype": "Currency", "width": 130},
        {"label": "Travel Budget", "fieldname": "travel_budget", "fieldtype": "Currency", "width": 130},
        {"label": "Travel Balance", "fieldname": "travel_balance", "fieldtype": "Currency", "width": 130},

        {"label": "Food Expense", "fieldname": "food_expense", "fieldtype": "Currency", "width": 130},
        {"label": "Food Budget", "fieldname": "food_budget", "fieldtype": "Currency", "width": 130},
        {"label": "Food Balance", "fieldname": "food_balance", "fieldtype": "Currency", "width": 130},

        {"label": "Stay Expense", "fieldname": "stay_expense", "fieldtype": "Currency", "width": 130},
        {"label": "Stay Budget", "fieldname": "stay_budget", "fieldtype": "Currency", "width": 130},
        {"label": "Stay Balance", "fieldname": "stay_balance", "fieldtype": "Currency", "width": 130},

        {"label": "Supply Expense", "fieldname": "supply_expense", "fieldtype": "Currency", "width": 130},
        {"label": "Supply Budget", "fieldname": "supply_budget", "fieldtype": "Currency", "width": 130},
        {"label": "Supply Balance", "fieldname": "supply_balance", "fieldtype": "Currency", "width": 130},

        {"label": "Service Expense", "fieldname": "service_expense", "fieldtype": "Currency", "width": 130},
        {"label": "Service Budget", "fieldname": "service_budget", "fieldtype": "Currency", "width": 130},
        {"label": "Service Balance", "fieldname": "service_balance", "fieldtype": "Currency", "width": 130},

        {"label": "Internal Costing", "fieldname": "internal_costing", "fieldtype": "Currency", "width": 150},

        {"label": "Total Expense", "fieldname": "total_expense", "fieldtype": "Currency", "width": 140},
        {"label": "Total Budget", "fieldname": "total_budget", "fieldtype": "Currency", "width": 140},
        {"label": "Total Balance", "fieldname": "total_balance", "fieldtype": "Currency", "width": 140},
    ]

    project_filters = {}
    if filters.get("project"):
        project_filters["name"] = filters["project"]

    projects = frappe.get_all("Project", filters=project_filters, fields=[
        "name", "project_name",
        "custom_total_expense_travel", "custom_travel_budget",
        "custom_total_expense_food", "custom_food_budget",
        "custom_total_expense_stay", "custom_stay_budget",
        "custom_total_expense_supply", "custom_supply_budget",
        "custom_total_expense_service", "custom_service_budget",
        "custom_total_internal_costing"
    ])

    data = []
    for p in projects:
        # Handle nulls
        travel_expense = p.custom_total_expense_travel or 0
        travel_budget = p.custom_travel_budget or 0
        food_expense = p.custom_total_expense_food or 0
        food_budget = p.custom_food_budget or 0
        stay_expense = p.custom_total_expense_stay or 0
        stay_budget = p.custom_stay_budget or 0
        supply_expense = p.custom_total_expense_supply or 0
        supply_budget = p.custom_supply_budget or 0
        service_expense = p.custom_total_expense_service or 0
        service_budget = p.custom_service_budget or 0
        internal_costing = p.custom_total_internal_costing or 0

        # Totals
        total_expense = travel_expense + food_expense + stay_expense + supply_expense + service_expense
        total_budget = travel_budget + food_budget + stay_budget + supply_budget + service_budget
        total_balance = total_budget - total_expense

        row = {
            "name": p.name,
            "project_name": p.project_name,

            "travel_expense": travel_expense,
            "travel_budget": travel_budget,
            "travel_balance": travel_budget - travel_expense,

            "food_expense": food_expense,
            "food_budget": food_budget,
            "food_balance": food_budget - food_expense,

            "stay_expense": stay_expense,
            "stay_budget": stay_budget,
            "stay_balance": stay_budget - stay_expense,

            "supply_expense": supply_expense,
            "supply_budget": supply_budget,
            "supply_balance": supply_budget - supply_expense,

            "service_expense": service_expense,
            "service_budget": service_budget,
            "service_balance": service_budget - service_expense,

            "internal_costing": internal_costing,

            "total_expense": total_expense,
            "total_budget": total_budget,
            "total_balance": total_balance,
        }
        data.append(row)

    return columns, data
