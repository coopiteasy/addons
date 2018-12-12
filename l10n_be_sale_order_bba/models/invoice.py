# © 2018 Coop IT Easy (http://www.coopiteasy.be)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    def generate_bbacomm(self, type, reference_type, partner_id, reference):
        if self.reference:
            return {'value': {'reference': self.reference}}
        else:
            return super(AccountInvoice, self).generate_bbacomm(type,
                                                                reference_type,
                                                                partner_id,
                                                                reference)
