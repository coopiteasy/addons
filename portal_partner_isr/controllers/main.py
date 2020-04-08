# Copyright 2018 Rémy Taymans <remytaymans@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import http
from odoo.http import request


class PortalISR(http.Controller):

    @http.route("/isr", type="http", auth="user", website=True)
    def isr(self):
        partner = request.env.user.partner_id
        if partner.isr_number:
            url = "https://tools.hsolutions.ch/outils/bvrlignon/?bvr=" + partner.isr_number
            return request.redirect(url)
        else:
            return request.redirect("my/credit_account")
