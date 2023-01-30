# SPDX-FileCopyrightText: 2023 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import fields, models


class ResourceBookingType(models.Model):
    _inherit = "resource.booking.type"

    default_product_id = fields.Many2one(
        comodel_name="product.product", string="Default Product"
    )
