# -*- coding: utf-8 -*-
# Copyright 2019 Coop IT Easy SCRL fs
#   Houssine Bakkali <houssine@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    bvr_number = fields.Char(
        string="BVR number",
        readonly=True
        )
    customer_number = fields.Integer(
        string="Customer ID",
        readonly=True
        )

    def get_customer_seq(self):
        return self.env.ref('partner_bvr.sequence_customer_id', False)

    def get_bvr_number(self, partner):
        number = 99999 - partner.customer_number
        bvr_number = '20' + str(number).rjust(5, '0')
        bvr_number = bvr_number + str(partner.customer_number).rjust(5, '0')
        bvr_number = bvr_number + '00000'

        return bvr_number

    @api.multi
    def action_generate_bvr(self):
        for partner in self:
            if partner.customer:
                if not partner.customer_number:
                    cust_sequ = self.get_customer_seq()
                    cust_number = cust_sequ.next_by_id()
                    partner.customer_number = cust_number
                if not partner.bvr_number:
                    partner.bvr_number = self.get_bvr_number(partner)
