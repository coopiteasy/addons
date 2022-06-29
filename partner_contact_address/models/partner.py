# Copyright 2018 Coop IT Easy SC.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    type = fields.Selection(
        selection_add=[("representative", "Representative")],
        default="representative",
    )
