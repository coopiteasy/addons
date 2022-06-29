# Copyright 2022 Coop IT Easy SC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductTemplate(models.Model):

    _inherit = "product.template"

    restrict_delivery_carrier_to = fields.Many2many(
        comodel_name="delivery.carrier",
        string="Restrict Delivery Carrier To",
        help="This product can only be shipped with the following "
        "delivery carrier. Left empty to allow all delivery carrier to "
        "be used.",
    )
