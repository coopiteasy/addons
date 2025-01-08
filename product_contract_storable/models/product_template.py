# SPDX-FileCopyrightText: 2025 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import models


class ContractContract(models.Model):
    _inherit = "product.template"

    def _check_contract_product_type(self):
        pass
