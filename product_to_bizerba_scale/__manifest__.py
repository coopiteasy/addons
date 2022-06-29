# Copyright 2014-2017 GRAP (http://www.grap.coop)
#   - Sylvain LE GAL (https://twitter.com/legalsylvain)
# Copyright 2017-Today Coop IT Easy SC
#   - Houssine BAKKALI <houssine@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Product to Bizerba Scale",
    "summary": """
        This module merges product_to_scale_bizerba and
        product_to_scale_bizerba_extended into one.
    """,
    "author": "Coop IT Easy SC, GRAP",
    "website": "https://coopiteasy.be",
    "category": "Tools",
    "version": "12.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["beesdoo_product", "sale_management"],
    "data": [
        "security/ir_module_category.xml",
        "security/res_groups.xml",
        "security/ir.model.access.csv",
        "data/ir_config_parameter.xml",
        "data/ir_cron.xml",
        "views/product_template_view.xml",
        "views/uom_uom_view.xml",
        "views/product_scale_system_view.xml",
        "views/product_scale_group_view.xml",
        "views/product_scale_log_view.xml",
        "views/action.xml",
        "views/menu.xml",
    ],
    "demo": [
        "demo/res_users.xml",
        "demo/product_scale_system.xml",
        "demo/product_scale_system_product_line.xml",
        "demo/product_scale_group.xml",
        "demo/product_template.xml",
        "demo/decimal_precision.xml",
    ],
}
