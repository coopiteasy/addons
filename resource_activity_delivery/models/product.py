# Copyright 2021 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


from openerp import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_delivery = fields.Boolean(string="Delivery")
