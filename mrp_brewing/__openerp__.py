# -*- coding: utf-8 -*-
# © 2016-2018 Open Architects Consulting SPRL.
# © 2018 Coop IT Easy SCRLfs. (<http://www.coopiteasy.be>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "MRP Brewing",
    "description": "This module allows to handle product transformation",
    "category": "Stock",
    "version": "9.0.1.0.0",
    "author": "Coop IT Easy SCRLfs",
    "website": "www.coopiteasy.be",
    "license": "AGPL-3",
    "depends": [
        "base",
        "mrp_byproduct",
        "stock",
        "sale",
        "product",
        "sale_order_dates",
        "purchase",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/brewing_data.xml",
        "data/cron.xml",
        "report/report_stock_raw_materials.xml",
        "report/report_stock_finished_products.xml",
        "report/report_brew_register.xml",
        "report/report_stock.xml",
        "report/report_layout.xml",
        "wizard/stock_reports_view.xml",
        "wizard/recompute_qty_afte_move_view.xml",
        "views/product_view.xml",
        "views/mrp_view.xml",
        "views/brew_view.xml",
        "views/stock_view.xml",
        "views/sale_view.xml",
        "views/sale_order_report.xml",
        "views/partner_view.xml",
        "views/company_view.xml",
    ],
    "application": True,
}
