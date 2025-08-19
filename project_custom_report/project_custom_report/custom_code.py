

import frappe
from frappe import _


@frappe.whitelist()
def get_bom_items_with_custom_fields(bom, qty, fetch_exploded=1, company=None):
    """
    Fetch BOM items including custom fields: custom_small_text, custom_long_text
    """
    from erpnext.manufacturing.doctype.bom.bom import get_bom_items

    # Get the BOM items using the standard method
    items = get_bom_items(bom=bom, qty=qty, fetch_exploded=fetch_exploded, company=company)

    # Add custom fields from BOM Item child table
    for item in items:
        # Fetch the BOM Item from the BOM using item_code
        bom_item = frappe.get_all("BOM Item", filters={"parent": bom, "item_code": item["item_code"]}, fields=["custom_small_text", "custom_long_text"])

        if bom_item:
            # Assuming the BOM Item has custom_small_text and custom_long_text fields
            item["custom_small_text"] = bom_item[0].get("custom_small_text", "")
            item["custom_long_text"] = bom_item[0].get("custom_long_text", "")

    return items

