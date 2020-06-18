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
    "name": "Resource Planning",
    "version": "1.0",
    "depends": ["base", "mail", "resource", "web_gantt8",],
    "author": "Houssine BAKKALI <houssine@coopiteasy.be>",
    "category": "Resource",
    "website": "www.coopiteasy.be",
    "license": "AGPL-3",
    "description": """
    This module manages the planning of the resources. It aims to provide an api in
    in order to be able to tie a resource with any other model.
    """,
    "data": [
        "data/resource_planning_data.xml",
        "security/resource_planning_security.xml",
        "security/ir.model.access.csv",
        "wizard/check_resource_availabilities_wizard.xml",
        "wizard/allocate_resource_wizard.xml",
        "views/resource_planning_views.xml",
        "views/resource_location_views.xml",
        "views/partner_views.xml",
        "views/res_config_view.xml",
        "views/actions.xml",
        "views/menus.xml",
    ],
    "installable": True,
    "application": True,
}
