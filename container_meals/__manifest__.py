# Copyright 2022 Coop IT Easy SC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Container Meals",
    "summary": """Deliver meals in containers.""",
    "version": "14.0.1.1.0",
    "category": "Uncategorized",
    "website": "https://coopiteasy.be",
    "author": "Coop IT Easy SC",
    "license": "AGPL-3",
    "application": False,
    "depends": [
        "partner_manual_rank",  # is_customer
        "product",
        "uom_extra_data",  # mL
        "website_sale",
    ],
    "excludes": [],
    "data": [
        "data/portion_attributes.xml",
        "views/product_views.xml",
        "views/res_config_settings_views.xml",
        "views/res_partner_views.xml",
        "views/sale_order_views.xml",
        "views/sale_menu.xml",
    ],
    "demo": [],
    "qweb": [],
}
