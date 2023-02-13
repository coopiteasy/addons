# SPDX-FileCopyrightText: 2023 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    resource_ids = fields.One2many(
        comodel_name="resource.resource",
        inverse_name="product_id",
        string="Resources",
    )
