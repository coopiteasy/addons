# -*- coding: utf-8 -*-
# Copyright 2019 Coop IT Easy SCRL fs
#   Houssine Bakkali <houssine@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models


class AccountBankStatement(models.Model):
    _inherit = "account.bank.statement"

    @api.multi
    def set_partner_on_bvr(self):
        self.ensure_one()
        if self.state == 'open':
            customers = self.env['res.partner'].search([
                                                ('customer', '=', True),
                                                ('bvr_number', '!=', False)
                                                ])
            for line in self.line_ids:
                partner = customers.filtered(lambda cust: cust.bvr_number == line.ref)
                if partner:
                    line.partner_id = partner.id
