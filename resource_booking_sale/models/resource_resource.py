# SPDX-FileCopyrightText: 2023 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import fields, models


class Resource(models.Model):
    _inherit = "resource.resource"

    product_id = fields.Many2one(
        "product.product",
        string="Product",
    )
