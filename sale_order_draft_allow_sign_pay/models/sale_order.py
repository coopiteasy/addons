# SPDX-FileCopyrightText: 2026 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _has_to_be_signed(self, include_draft=False):
        return super()._has_to_be_signed(True)

    def _has_to_be_paid(self, include_draft=False):
        return super()._has_to_be_paid(True)
