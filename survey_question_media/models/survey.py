# -*- coding: utf-8 -*-
##############################################################################
#
#    BOSS, Business Open Source Solution
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
from openerp.osv import fields, orm

class survey_question(orm.Model):

    _inherit = 'survey.question'

    _columns = {
        'image': fields.binary("Image",
            help="This field holds the image used as image for the question, limited to 1024x1024px."),
        'video_url': fields.char("Video Url", size=264,
            help="This field holds the video url used as video for the question"),
    }