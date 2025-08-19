

import frappe
from frappe import _

@frappe.whitelist()
def get_bom_items_with_custom_fields(bom, qty, fetch_exploded=1, company=None):
    """
    Fetch BOM items including custom fields: custom_small_text, custom_long_text
    """
    from erpnext.manufacturing.doctype.bom.bom import get_bom_items

    items = get_bom_items(bom=bom, qty=qty, fetch_exploded=fetch_exploded, company=company)

    # Add custom fields from BOM child table
    for i in items:
        bom_item = frappe.get_doc("BOM Item", {"parent": bom, "item_code": i.get("item_code")})
        i["custom_small_text"] = bom_item.custom_small_text
        i["custom_long_text"] = bom_item.custom_long_text

    return items
