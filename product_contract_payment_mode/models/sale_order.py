# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later


from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _prepare_contract_value(self, contract_template):
        self.ensure_one()
        values = super()._prepare_contract_value(contract_template)
        values["payment_mode_id"] = self.payment_mode_id.id
        return values
