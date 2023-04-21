# SPDX-FileCopyrightText: 2023 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    packaging_product_ids = fields.Many2many(
        comodel_name="product.product",
        string="Packaging Products",
        help="Products that are added to the packaging section of a sales order"
        " by default.",
        related="company_id.packaging_product_ids",
        readonly=False,
    )
