# Copyright 2019 Coop IT Easy SC
#   Houssine Bakkali <houssine@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


from odoo import api, fields, models
from odoo.tools.misc import mod10r


class ResPartner(models.Model):
    _inherit = "res.partner"

    isr_number = fields.Char(string="ISR number", readonly=True)
    customer_number = fields.Integer(string="Customer ID", readonly=True)

    _sql_constraints = [
        (
            "customer_number_uniq",
            "unique(customer_number, company_id)",
            "Customer number must be unique",
        ),
    ]

    _sql_constraints = [
        (
            "isr_number_uniq",
            "unique(isr_number, company_id)",
            "ISR number must be unique",
        ),
    ]

    def get_customer_seq(self):
        return self.env.ref("partner_isr.sequence_customer_id", False)

    def get_isr_number(self, partner):
        number = 99999 - partner.customer_number
        isr_number = "20" + str(number).rjust(5, "0")
        isr_number = isr_number + str(partner.customer_number).rjust(5, "0")
        isr_number = isr_number + "00000"

        return mod10r(isr_number)

    @api.multi
    def action_generate_isr(self):
        for partner in self:
            if partner.customer:
                if not partner.customer_number:
                    cust_sequ = self.get_customer_seq()
                    cust_number = cust_sequ.next_by_id()
                    partner.customer_number = cust_number
                if not partner.isr_number:
                    partner.isr_number = self.get_isr_number(partner)
