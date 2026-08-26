# Copyright 2021 Coop IT Easy SC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResourceResource(models.Model):
    _inherit = "resource.resource"

    # force this field to be equal to the resource_calendar_id of the company.
    calendar_id = fields.Many2one(
        "resource.calendar",
        # this is to prevent the warning:
        # odoo.fields: Redundant default on resource.resource.calendar_id
        # (coming from odoo.fields.Field.setup_related()). this is because
        # company_id has the default value: lambda self: self.env.company, and
        # with this argument, this fields gets an automatic default value of
        # lambda self: self.env.company.resource_calendar_id.
        default=None,
        related="company_id.resource_calendar_id",
        store=True,
    )
