# -*- coding: utf-8 -*-
##############################################################################
#
#    Business Open Source Solution
#    Copyright (C) 2018- Coop IT Easy SCRL.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    "name": "Resource activity",
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
    "author": "Houssine BAKKALI <houssine@coopiteasy.be>",
    "category": "Resource",
    "website": "www.coopiteasy.be",
    "license": "AGPL-3",
    "description": """
    This allows to manage sale activities on your resources.
    """,
    "data": [
        "security/ir.model.access.csv",
        "data/resource_activity_data.xml",
        "data/cron.xml",
        "views/partner_views.xml",
        "views/product_views.xml",
        "views/res_company_views.xml",
        "views/resource_activity_delivery_views.xml",
        "views/resource_activity_lang_views.xml",
        "views/resource_activity_registration_views.xml",
        "views/resource_activity_theme_views.xml",
        "views/resource_activity_type_views.xml",
        "views/resource_activity_views.xml",
        "views/resource_allocation_views.xml",
        "views/resource_category_views.xml",
        "views/resource_location_views.xml",
        "views/resource_resource_views.xml",
        "views/sale_note_views.xml",
        "views/sale_order_views.xml",
        "views/terms_conditions_views.xml",
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
