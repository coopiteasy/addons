# Copyright 2022 Coop IT Easy SC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, fields, models
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval


class DeliveryCarrier(models.Model):

    _inherit = "delivery.carrier"

    combine_type = fields.Selection(
        [("or", "OR (default)"), ("and", "AND")],
        required=True,
        default="or",
        help=(
            "OR: compute price based on the first rule that is evaluate true. "
            "AND: compute price by summing price for each rule. All rules "
            "must be evaluated true else the delivery cannot apply."
        ),
    )

    def _get_price_from_picking(self, total, weight, volume, quantity):
        if self.combine_type == "or":
            price = super()._get_price_from_picking(total, weight, volume, quantity)
        elif self.combine_type == "and":
            price = 0.0
            criteria_false = False
            price_dict = {
                "price": total,
                "volume": volume,
                "weight": weight,
                "wv": volume * weight,
                "quantity": quantity,
            }
            for line in self.price_rule_ids:
                test = safe_eval(
                    line.variable + line.operator + str(line.max_value),
                    price_dict,
                )
                if test:
                    price += (
                        line.list_base_price
                        + line.list_price * price_dict[line.variable_factor]
                    )
                else:
                    criteria_false = True
                    break
            if criteria_false:
                raise UserError(
                    _(
                        "At least one price rule does not match this order; "
                        "delivery cost cannot be computed."
                    )
                )
        return price
