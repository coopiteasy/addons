# Copyright 2017 - Today Coop IT Easy SCRLfs (<http://www.coopiteasy.be>)
# - Houssine Bakkali <houssine@coopiteasy.be>
# Copyright (c) 2011 Noviat nv/sa (www.noviat.be).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import re

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    bypass_check_bbacom = fields.Boolean(string="By pass the bba com validation")

    def check_bbacomm(self):
        self.ensure_one()
        pattern = re.compile(r"^\+\+\+\d{3}/\d{4}/\d{5}\+\+\+$")
        if not pattern.fullmatch(self.reference or ""):
            raise ValidationError(
                _(
                    "Invalid structured communication for %s. "
                    "Please enter a reference with the form "
                    "+++.../..../.....+++." % self.reference
                )
            )
        bbacomm = re.sub(r"\D", "", self.reference or "")
        if len(bbacomm) == 12:
            base = int(bbacomm[:10])
            mod = base % 97 or 97
            if mod == int(bbacomm[-2:]):
                return True
        raise ValidationError(
            _("Invalid structured communication for %s" % self.reference)
        )

    @api.multi
    def invoice_validate(self):
        company = self.mapped("company_id")
        if company.invoice_reference_type == "structured":
            for invoice in self:
                if (
                    not invoice.bypass_check_bbacom
                    and invoice.reference
                    and invoice.type == "in_invoice"
                ):
                    invoice.check_bbacomm()
        super(AccountInvoice, self).invoice_validate()
