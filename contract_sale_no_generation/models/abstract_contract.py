# SPDX-FileCopyrightText: 2025 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import fields, models


class ContractAbstractContract(models.AbstractModel):
    _inherit = "contract.abstract.contract"

    generation_type = fields.Selection(
        selection_add=[("none", "None")],
    )
