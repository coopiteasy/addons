# Copyright 2014-2017 GRAP (http://www.grap.coop)
#   - Sylvain LE GAL (https://twitter.com/legalsylvain)
# Copyright 2017-Today Coop IT Easy SC
#   - Houssine BAKKALI <houssine@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class Uom(models.Model):
    _inherit = "uom.uom"

    scale_type = fields.Char(string="Scale Type")
