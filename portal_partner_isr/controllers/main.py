# Copyright 2018 Rémy Taymans <remytaymans@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import http
from odoo.http import request
from urllib.parse import quote_plus


class PortalISR(http.Controller):

    @http.route("/isr", type="http", auth="user", website=True)
    def isr(self):
        partner = request.env.user.partner_id
        if partner.isr_number:
            url = "https://tools.hsolutions.ch/outils/bvrlignon/"
            url += "?bvr=" + partner.isr_number
            url += "&name=" + quote_plus(partner.name) if partner.name else ""
            url += "&street=" + quote_plus(partner.street) if partner.street else ""
            url += "&zip=" + quote_plus(partner.zip) if partner.zip else ""
            url += "&city=" + quote_plus(partner.city) if partner.city else ""
            return request.redirect(url)
        else:
            return request.redirect("my/credit_account")
