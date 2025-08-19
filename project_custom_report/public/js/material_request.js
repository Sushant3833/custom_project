frappe.ui.form.on('Material Request', {
    refresh: function(frm) {
        // Add custom button in the top bar
        frm.add_custom_button(__('Get Items from BOM'), function() {
            get_items_from_bom(frm);
        }, __('Get Items from BOM'));
    }
});

// Function to fetch items from BOM
function get_items_from_bom(frm) {
    var d = new frappe.ui.Dialog({
        title: __("Get Items from BOM"),
        fields: [
            {
                fieldname: "bom",
                fieldtype: "Link",
                label: __("BOM"),
                options: "BOM",
                reqd: 1,
                get_query: function () {
                    return { filters: { docstatus: 1, is_active: 1 } };
                },
            },
            {
                fieldname: "warehouse",
                fieldtype: "Link",
                label: __("For Warehouse"),
                options: "Warehouse",
                reqd: 1,
            },
            { 
                fieldname: "qty", 
                fieldtype: "Float", 
                label: __("Quantity"), 
                reqd: 1, 
                default: 1 
            },
            {
                fieldname: "fetch_exploded",
                fieldtype: "Check",
                label: __("Fetch exploded BOM (including sub-assemblies)"),
                default: 1,
            },
        ],
        primary_action_label: __("Get Items"),
        primary_action(values) {
            if (!values) return;
            values["company"] = frm.doc.company;
            if (!frm.doc.company) frappe.throw(__("Company field is required"));

            frappe.call({
                method: "project_custom_report.project_custom_report.custom_code.get_bom_items_with_custom_fields",
                args: values,
                callback: function (r) {
                    if (!r.message) {
                        frappe.throw(__("BOM does not contain any stock item"));
                    } else {
                        erpnext.utils.remove_empty_first_row(frm, "items");
                        console.log("Right  function#####")
                        $.each(r.message, function (i, item) {
                            var row = frappe.model.add_child(frm.doc, "Material Request Item", "items");
            
                            row.item_code = item.item_code;
                            row.item_name = item.item_name;
                            row.description = item.description;
                            row.warehouse = values.warehouse;
                            row.uom = item.stock_uom;
                            row.stock_uom = item.stock_uom;
                            row.conversion_factor = 1;
                            row.qty = item.qty;
                            row.project = item.project;
            
                            // Custom fields
                            row.custom_small_text = item.custom_small_text || "";
                            row.custom_long_text = item.custom_long_text || "";
                        });
                    }
                    d.hide();
                    refresh_field("items");
                }
            });
            
        },
    });

    d.show();
}
