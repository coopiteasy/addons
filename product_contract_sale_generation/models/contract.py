# SPDX-FileCopyrightText: 2025 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import models


class ContractContract(models.Model):
    _inherit = "contract.contract"

    def _prepare_recurring_sales_values(self, date_ref=False):
        sale_order_vals_list = super()._prepare_recurring_sales_values(date_ref)
        for sale_order_vals in sale_order_vals_list:
            sale_order_vals["created_from_contract"] = True
        return sale_order_vals_list
