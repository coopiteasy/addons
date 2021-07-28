# Copyright 2021 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


from openerp import api, fields, models


class ResourceActivityRegistration(models.Model):
    _inherit = "resource.activity.registration"

    date_start = fields.Datetime(
        help="The soonest date between activity start date and delivery time."
        " Set to 90m before date start if set manually"
        " and delivery needed."
    )
    date_end = fields.Datetime(
        help="The latest date between activity end and pickup time."
        " Set to 90m after date end if set manually"
        " and delivery needed."
    )
