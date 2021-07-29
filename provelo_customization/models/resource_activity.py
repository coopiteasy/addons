# Copyright 2021 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


from odoo import api, fields, models


class ResourceActivity(models.Model):
    _inherit = "resource.activity"

    @api.multi
    def action_done(self):
        """
        Allowed from
        - sale state
        - draft state if nothing to invoice
        - allow but warn from draft state with invoiced resources
        """
        for activity in self:
            registrations = activity.registrations.filtered(
                lambda r: r.state in ["option", "booked"]
            )
            # warn if in draft and invoiced resources booked
            if activity.state == "draft" and (
                    registrations or activity.guides or activity.trainers
            ):
                action = self.env.ref("resource_activity.action_draft_to_done")
                return {
                    "name": action.name,
                    "help": action.help,
                    "type": action.type,
                    "view_type": action.view_type,
                    "view_mode": action.view_mode,
                    "target": action.target,
                    "context": self._context,
                    "res_model": action.res_model,
                }
            elif activity.state in ("draft", "sale"):
                activity.state = "done"