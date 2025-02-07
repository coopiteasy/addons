# Copyright 2022 Coop IT Easy SC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class ChooseDeliveryCarrier(models.TransientModel):

    _inherit = "choose.delivery.carrier"

    @api.depends("partner_id", "order_id.order_line")
    def _compute_available_carrier(self):
        result = super()._compute_available_carrier()
        delivery_carrier_model = self.env["delivery.carrier"]
        for rec in self:
            products = list(rec.order_id.order_line.mapped("product_id"))
            # this method is called at 2 different times:
            # 1. when opening the wizard.
            # 2. when confirming the wizard.
            # in the 1st case, rec.available_carrier_ids is not a recordset
            # with actual ids, but with ids of type <NewId origin=...>, where
            # origin is the actual id. in the 2nd case, they have actual ids.
            # we need to handle both cases correctly.
            ids = [r.id for r in rec.available_carrier_ids]
            if len(ids) > 0 and not isinstance(ids[0], int):
                ids = [id.origin for id in ids]
            available_carrier_ids = delivery_carrier_model.browse(ids)
            rec.available_carrier_ids = available_carrier_ids.filtered(
                lambda c: c._can_be_used_to_deliver_products(products)
            )
        # this is just to silence W8110
        return result
