# Copyright 2021 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


from openerp import models


class ResourceActivity(models.Model):
    _inherit = "resource.activity"

    def _create_sale_order(self, activity, partner_id):
        order = super(ResourceActivity, self)._create_sale_order(
            activity, partner_id
        )
        sale_note_html = (
            activity.location_id.terms_ids.filtered(
                lambda r: r.note_id.active
                and r.location_id == activity.location_id
                and r.activity_type_id == activity.activity_type
            ).note_id.content
            or self.env["sale.order"]._default_note_html()
        )
        order.note_html = sale_note_html
        return order
