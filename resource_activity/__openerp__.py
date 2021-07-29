# -*- coding: utf-8 -*-
# Copyright 2021 Coop IT Easy SCRL fs
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Resource Activity",
    "version": "9.0.1.0.1",
    "depends": [
        "base",
        "mail",
        "resource_planning",
        "theme_light",
        "product",
        "sale",
        "web_tree_many2one_clickable",
        "web_tree_dynamic_colored_field",
    ],
    "author": "Coop IT Easy SCRLfs",
    "category": "Resource",
    "website": "https://www.coopiteasy.be",
    "license": "AGPL-3",
    "description": """
        Manage activities, book resources and generate sale orders.
    """,
    "data": [
        "security/ir.model.access.csv",
        "data/resource_activity_data.xml",
        "data/cron.xml",
        "views/partner_views.xml",
        "views/product_views.xml",
        "views/resource_activity_lang_views.xml",
        "views/resource_activity_registration_views.xml",
        "views/resource_activity_theme_views.xml",
        "views/resource_activity_type_views.xml",
        "views/resource_activity_views.xml",
        "views/resource_allocation_views.xml",
        "views/resource_category_views.xml",
        "views/resource_location_views.xml",
        "views/resource_resource_views.xml",
        "views/sale_order_views.xml",
        "wizard/activity_draft_to_done.xml",
        "wizard/cancel_sale_order_wizard.xml",
        "reports/resource_activity_reports.xml",
        "reports/activity_registration_report.xml",
        "reports/activity_report.xml",
        "reports/sale_order_report.xml",
        "reports/layouts.xml",
        "views/menus.xml",
    ],
    "demo": [
        "demo/demo.xml",
    ],
    "installable": True,
    "application": True,
}
