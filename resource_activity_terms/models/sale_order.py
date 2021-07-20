# -*- coding: utf-8 -*-
# Copyright 2018 Coop IT Easy SCRLfs.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.model
    def _default_note_html(self):
        return self.env.user.company_id.sale_note_html

    note_html = fields.Html(
        "Terms and conditions", default=lambda self: self._default_note_html()
    )
