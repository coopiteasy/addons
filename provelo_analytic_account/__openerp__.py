# -*- coding: utf-8 -*-
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
    "name": "Provelo Analytic Account",
    "version": "9.0.1.0.0",
    "depends": ["hr", "resource_activity",],
    "author": "Coop IT Easy SCRLfs",
    "license": "AGPL-3",
    "category": "",
    "website": "www.coopiteasy.be",
    "description": """
        Match BOB analytical accounts.
    """,
    "data": [
        "security/ir.model.access.csv",
        "views/hr_department.xml",
        "views/provelo_financing.xml",
        "views/provelo_project.xml",
        "views/resource_location.xml",
        "views/actions.xml",
        "views/menus.xml",
    ],
    "installable": True,
}
