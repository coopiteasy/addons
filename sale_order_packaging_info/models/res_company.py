# SPDX-FileCopyrightText: 2023 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    packaging_product_ids = fields.Many2many(
        comodel_name="product.product",
        # Manually defined relation table to not conflict with other M2M
        # relations between the same models.
        relation="res_company_product_product_packaging_rel",
        string="Packaging Products",
    )
