# Copyright 2018 - Today Coop IT Easy SC (<http://www.coopiteasy.be>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


from odoo import fields, models


class Website(models.Model):
    _inherit = "website"

    display_document_page = fields.Boolean("Display documents on website", default=True)
