# -*- coding: utf-8 -*-
# Copyright 2019 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models, _


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    @api.model
    def reset_so_line(self):
        lines = self.search([("so_line.order_id.state", "=", "sale")])
        for line in lines:
            vals = {
                "product_uom_id": line.product_uom_id.id,
                "amount": -0.0,
                "account_id": line.account_id.id,
            }
            res = line.sudo()._get_sale_order_line(vals=vals)
            line.write(vals)
            print(res)

        lines.mapped("so_line").sudo()._compute_analytic()
        return lines
