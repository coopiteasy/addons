# SPDX-FileCopyrightText: 2026 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import fields, models


class ProductMarginClassification(models.Model):
    _inherit = "product.margin.classification"

    # the price surcharge is applied to the unit price
    # so it should be defined by unit rather than by box.
    price_surcharge = fields.Float("Unit Price Surcharge")
