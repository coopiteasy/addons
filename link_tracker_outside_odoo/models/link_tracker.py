# -*- coding: utf-8 -*-
from urlparse import urlparse
from openerp import models, fields, api

class LinkTracker(models.Model):
    """link_tracker allow users to wrap any URL into a short and trackable URL.
    link_tracker counts clicks on each tracked link.
    This module is also used by mass_mailing, where each link in mail_mail html_body are converted into
    a trackable link to get the click-through rate of each mass_mailing."""

    _inherit = "link.tracker"

    @api.one
    @api.depends('url')
    def _compute_redirected_url(self):
        web_base_url = self.env['ir.config_parameter'].get_param('web.base.url')
        
        parsed = urlparse(self.url)

        utms = {}
        for key, field, cook in self.env['utm.mixin'].tracking_fields():
            attr = getattr(self, field).name
            if attr:
                utms[key] = attr
        
        if '%s://%s' % (parsed.scheme, parsed.netloc) == web_base_url:
            self.redirected_url = '%s://%s%s?%s&%s#%s' % (parsed.scheme, parsed.netloc, parsed.path, url_encode(utms), parsed.query, parsed.fragment)
        else:
            self.redirected_url = '%s://%s%s' % (parsed.scheme, parsed.netloc, parsed.path)
