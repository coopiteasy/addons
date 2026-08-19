# SPDX-FileCopyrightText: 2026 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import fields, models


class MisBudgetItemAbstract(models.AbstractModel):
    _inherit = "mis.budget.item.abstract"

    analytic_account_id = fields.Many2one(
        comodel_name="account.analytic.account", string="Analytic account"
    )

    def _prepare_overlap_domain(self):
        """Prepare a domain to check for overlapping budget items."""
        domain = super()._prepare_overlap_domain()
        domain.extend([("analytic_account_id", "=", self.analytic_account_id.id)])
        return domain
