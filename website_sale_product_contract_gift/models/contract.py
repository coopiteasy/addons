# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later


from odoo import fields, models


class ContractContract(models.Model):
    _inherit = "contract.contract"

    is_gift = fields.Boolean()

    def _recurring_create_invoice(self, date_ref=False):
        invoices = super()._recurring_create_invoice(date_ref=date_ref)
        invoices.create_user_for_gift()
        return invoices
