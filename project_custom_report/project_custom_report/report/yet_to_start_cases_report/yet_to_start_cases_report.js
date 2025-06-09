// Copyright (c) 2025, sushant and contributors
// For license information, please see license.txt

frappe.query_reports["Yet To Start cases Report"] = {
	"filters": [
        {
            "fieldname": "project",
            "label": "Project",
            "fieldtype": "Link",
            "options": "Project",
            "reqd": 0
        },
        {
            "fieldname": "fiscal_year",
            "label": "Fiscal Year",
            "fieldtype": "Link",
            "options": "Fiscal Year",
            "default": frappe.defaults.get_user_default("fiscal_year"),
            "reqd": 1
        }
    ]
};
