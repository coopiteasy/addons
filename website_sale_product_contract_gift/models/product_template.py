# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_gift = fields.Boolean()
