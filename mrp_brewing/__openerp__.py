# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2013-2016 Open Architects Consulting SPRL.
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
    'name': 'MRP Brewing',
    'description': 'Allows to print traceability reports on the stock moves',
    'category': 'Stock',
    'version': '1.0',
    'author': 'Coop IT Easy SCRLfs',
    'depends': ['base',
                'mrp_byproduct',
                'stock',
                'sale',
                'product',
                'sale_order_dates',
                ],
    'data': [
        'security/ir.model.access.csv',
        'data/brewing_data.xml',
        'data/cron.xml',
        'report/report_stock_raw_materials.xml',
        'report/report_stock_finished_products.xml',
        'report/report_brew_register.xml',
        'report/report_stock.xml',
        'report/report_layout.xml',
        'wizard/stock_reports_view.xml',
        'wizard/recompute_qty_afte_move_view.xml',
        'views/product_view.xml',
        'views/mrp_view.xml',
        'views/brew_view.xml',
        'views/stock_view.xml',
        'views/sale_view.xml',
        'views/sale_order_report.xml',
        'views/partner_view.xml',
    ],
    'application': True,
}
