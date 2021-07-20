# Copyright 2021 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


from openerp import api, fields, models


class ResourceActivity(models.Model):
    _inherit = "resource.activity"

    is_start_outside_opening_hours = fields.Boolean(
        string="Activity start is outside opening hours",
        compute="_compute_outside_opening_hours",
    )
    is_end_outside_opening_hours = fields.Boolean(
        string="Activity end is outside opening hours",
        compute="_compute_outside_opening_hours",
    )

    @api.multi
    @api.depends("date_end", "date_start", "location_id")
    def _compute_outside_opening_hours(self):
        opening_hours = self.env["activity.opening.hours"]
        for activity in self:
            if activity.date_start and activity.date_end:
                activity.is_start_outside_opening_hours = not (
                    opening_hours.is_location_open(
                        activity.location_id, activity.date_start
                    )
                )
                activity.is_end_outside_opening_hours = not (
                    opening_hours.is_location_open(
                        activity.location_id, activity.date_end
                    )
                )
