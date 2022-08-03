##############################################################################
#
#    Copyright (C) 2017- Coop IT Easy.
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
    "name": "Sale Order Volume",
    "version": "12.0.1.1.1",
    "depends": ["sale", "stock", "website_sale"],
    "author": "Coop IT Easy SC",
    "license": "AGPL-3",
    "category": "Sale",
    "website": "https://coopiteasy.be",
    "summary": """
    Computes the volume of products per
    category ordered and display it on
    """,
    "data": [
        "data/pallet_volume_data.xml",
        "views/sale_order.xml",
        "views/shopping_cart.xml",
        "reports/report_saleorder.xml",
        "views/res_config_settings_views.xml",
        "security/ir.model.access.csv",
    ],
    "demo": ["demo/demo.xml"],
    "installable": True,
}
