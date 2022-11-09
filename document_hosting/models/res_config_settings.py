# Copyright 2018 - Today Coop IT Easy SC (<http://www.coopiteasy.be>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    display_document_page = fields.Boolean(
        related="website_id.display_document_page", readonly=False
    )
