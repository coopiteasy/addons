# -*- coding: utf-8 -*-

from openerp import _, api, fields, models
import random
from urlparse import urljoin

class EventEvent(models.Model):
    
    _inherit = 'event.event'
    
    token = fields.Char(string="Token", readonly=True)
    event_attendance_url = fields.Char(string="Event attendance url", readonly=True)
    
    def _random_token(self):
        # the token has an entropy of about 120 bits (6 bits/char * 20 chars)
        chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
        return ''.join(random.SystemRandom().choice(chars) for i in xrange(20))
    
    @api.one
    def button_confirm(self):
        super(EventEvent,self).button_confirm()
        
        base_url = self.env['ir.config_parameter'].get_param('web.base.url')
        route = "/event/attendance"
        token =  self._random_token()
        
        self.token = token 
        self.event_attendance_url = urljoin(base_url, "%s?token=%s" % (route, token))
    
    @api.one
    def send_event_attendance_mail(self):
        return True