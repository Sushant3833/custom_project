# import datetime

# import frappe
# from frappe import _
# from frappe.model.workflow import get_workflow_name
# from frappe.query_builder.functions import Max, Min, Sum
# from frappe.utils import (
# 	add_days,
# 	cint,
# 	cstr,
# 	date_diff,
# 	flt,
# 	formatdate,
# 	get_fullname,
# 	get_link_to_form,
# 	getdate,
# 	nowdate,
# )

# from erpnext.buying.doctype.supplier_scorecard.supplier_scorecard import daterange
# from erpnext.setup.doctype.employee.employee import get_holiday_list_for_employee

# import hrms
# from hrms.api import get_current_employee_info
# from hrms.hr.doctype.leave_block_list.leave_block_list import get_applicable_block_dates
# from hrms.hr.doctype.leave_ledger_entry.leave_ledger_entry import create_leave_ledger_entry
# from hrms.hr.utils import (
# 	get_holiday_dates_for_employee,
# 	get_leave_period,
# 	set_employee_name,
# 	share_doc_with_approver,
# 	validate_active_employee,
# )
# from hrms.mixins.pwa_notifications import PWANotificationsMixin
# from hrms.utils import get_employee_email


# class LeaveDayBlockedError(frappe.ValidationError):
# 	pass


# class OverlapError(frappe.ValidationError):
# 	pass


# class AttendanceAlreadyMarkedError(frappe.ValidationError):
# 	pass


# class NotAnOptionalHoliday(frappe.ValidationError):
# 	pass


# class InsufficientLeaveBalanceError(frappe.ValidationError):
# 	pass


# class LeaveAcrossAllocationsError(frappe.ValidationError):
# 	pass


# from frappe.model.document import Document

# from hrms.hr.doctype.leave_application.leave_application import LeaveApplication

# class CustomLeaveApplication(LeaveApplication):
# 	def validate_dates_across_allocation(self):
# 		if frappe.db.get_value("Leave Type", self.leave_type, "allow_negative"):
# 			return

# 		alloc_on_from_date, alloc_on_to_date = self.get_allocation_based_on_application_dates()

# 		if not (alloc_on_from_date or alloc_on_to_date):
# 			pass
# 			# frappe.throw(_("Application period cannot be outside leave allocation period"))
# 		elif self.is_separate_ledger_entry_required(alloc_on_from_date, alloc_on_to_date):
# 			frappe.throw(
# 				_("Application period cannot be across two allocation records"),
# 				exc=LeaveAcrossAllocationsError,
# 			)