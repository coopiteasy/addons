# Copyright 2021 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


from openerp import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    is_guide = fields.Boolean(string="Guide")
    resource_location_guide = fields.Many2one(
        "resource.location", string="Guide Location"
    )
