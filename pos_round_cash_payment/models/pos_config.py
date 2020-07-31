# Copyright 2016 Robin Keunen, Coop IT Easy SCRL fs
# Copyright 2020 Houssine Bakkali, Coop IT Easy SCRL fs
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class PosConfig(models.Model):
    _inherit = "pos.config"

    cash_rounding_activated = fields.Boolean(
        string="Activate Cash Rounding", default=False
    )
