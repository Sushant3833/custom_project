// Copyright (c) 2025, sushant and contributors
// For license information, please see license.txt

frappe.query_reports["Project Budget"] = {
	"filters": [
		{
            "fieldname": "project",
            "label": "Project",
            "fieldtype": "Link",
            "options": "Project",
            "reqd": 0
        }

	]
};
