# SPDX-FileCopyrightText: 2025 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import models


class ContractContract(models.AbstractModel):
    _inherit = "contract.contract"

    def _reccuring_create_none(self):
        """
        This method triggers the creation of the invoices of the contracts of
        type "None" (currently empty to create no invoice)
        """
        return

    def _get_recurring_create_func(self, create_type="invoice"):
        """
        Allows to retrieve the recurring create function depending
        on generate_type attribute
        """
        if create_type == "none":
            return self.__class__._recurring_create_none
        return super()._get_recurring_create_func(create_type)
