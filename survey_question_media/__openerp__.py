# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2013-2015 Open Architects Consulting SPRL.
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
    'name': 'Survey Question Media',
    'description': 'This module aim to add multimedia (image, video) to a question',
    'category': 'Survey',
    'version': '1.0',
    'author': 'Houssine BAKKALI',
    'depends': ['base','survey'],
    'data': [
        'view/survey_templates.xml',
        'view/survey_views.xml',
    ],
    'installable' : True,
}