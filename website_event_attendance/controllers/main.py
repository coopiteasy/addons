# -*- coding: utf-8 -*-
# � 2017 Coop IT Easy (http://www.coopiteasy.be)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#import logging

#import datetime
from openerp.addons.web import http
from openerp.addons.web.http import request
from openerp import SUPERUSER_ID
from openerp.tools.translate import _
#from openerp import tools
from openerp.addons.website_event.controllers.main import website_event

#from openerp.exceptions import UserError

#_logger = logging.getLogger(__name__)

class WebsiteEvent(website_event):
    
    @http.route(['/event/attendance'], type='http', auth="public", website=True)
    def event_attendance(self, **post):
        env = request.env
        token = request.params.get('token')
        if token:
            event = env['event.event'].sudo().search([('token','=',token)])
            if len(event) > 0:
                values = {
                    'event': event,
                    'main_object': event,
                    'range': range,
                }
                return request.website.render("website_event_attendance.event_attendance", values)
        return request.website.render("website_event_attendance.event_attendance_error")