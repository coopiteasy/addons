# Copyright 2021 Coop IT Easy SC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResourceCalendarLeaves(models.Model):

    _inherit = "resource.calendar.leaves"

    # force this field to be equal to the resource_calendar_id of the resource
    # (which should be equal to the one of the company). this ensures that all
    # leaves for all resources are defined in the same resource calendar,
    # which is needed to compute working hours while taking leaves into
    # account.
    calendar_id = fields.Many2one(
        "resource.calendar",
        related="resource_id.calendar_id",
        readonly=True,
        store=True,
    )
