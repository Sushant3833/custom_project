// Copyright (c) 2025, sushant and contributors
// For license information, please see license.txt

frappe.query_reports["Project Expense Budget Balance"] = {
	"filters": [
		{
			"fieldname": "project",
			"label": "Project",
			"fieldtype": "Link",
			"options": "Project",
			"default": "",
			"reqd": 0
		  }

	]
};
