# Copyright 2021 Coop IT Easy SC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResourceResource(models.Model):

    _inherit = "resource.resource"

    # force this field to be equal to the resource_calendar_id of the company.
    # fixme A readonly related field without an inverse method should not have a
    #      default value, as it does not make sense.
    #      cf odoo/odoo/fields.py:626

    calendar_id = fields.Many2one(
        "resource.calendar",
        related="company_id.resource_calendar_id",
        readonly=True,
        store=True,
    )
