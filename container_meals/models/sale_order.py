# Copyright 2022 Coop IT Easy SCRL fs
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import logging
from collections import namedtuple

from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.translate import _

ContainerVolumes = namedtuple(
    "ContainerVolumes", ["container_1_volume", "container_2_volume"]
)
_EMPTY = ContainerVolumes(0, 0)

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    # Used for views.
    contains_containers = fields.Boolean(
        string="Contains Containers",
        compute="_compute_contains_containers",
    )

    @api.depends("order_line", "order_line.product_id")
    def _compute_contains_containers(self):
        for order in self:
            order.contains_containers = bool(
                order.order_line.filtered("product_id.is_container")
            )

    def calculate_volume_containers(self):
        """For every product template found in this sale order that
        is a meal, return a tuple (combined_container_1_volume,
        combined_container_2_volume).

        Example: The sale order contains two adult portions of the salad
        template, and one child portion. The volumes for the salad containers
        are (900, 600), and (600, 400) for the child portion. This function will
        return ``{product.template(salad,): (900*2+600, 600*2+400)}``.
        """
        self.ensure_one()
        result = dict()
        for line in self.order_line:
            product_id = line.product_id
            product_template = product_id.product_tmpl_id
            if product_id.is_meal:
                vols = result.setdefault(product_template, _EMPTY)
                # TODO: Account for the container's uom, maybe
                result[product_template] = ContainerVolumes(
                    vols.container_1_volume
                    + (product_id.container_1_volume * line.product_uom_qty),
                    vols.container_2_volume
                    + (product_id.container_2_volume * line.product_uom_qty),
                )
        return result

    def find_containers_for_volume(self, volume):
        """Given a volume, find a list of containers that will hold it.

        Example: TODO

        Important to note is that the list may:

        - include 0 items (volume is (sub-)zero)
        - include 1 item (volume fits into one container)
        - include more than 2 items (need more containers to hold the total
          volume)
        """
        self.ensure_one()

        result = []
        if volume <= 0:
            return result

        containers = (
            self.env["product.template"]
            .search([("is_container", "=", True)])
            .sorted(key="container_volume")
        )

        biggest_volume = containers[-1].container_volume
        quotient, remainder = divmod(volume, biggest_volume)

        result.extend(int(quotient) * [containers[-1].product_variant_id])

        for container in containers:
            if container.container_volume >= remainder:
                result.append(container.product_variant_id)
                break

        return result

    def add_containers(self):
        self.ensure_one()
        self._remove_containers()

        template_volumes_dict = self.calculate_volume_containers()
        containers_to_add = {}  # container: amount
        total_container_price = 0

        for volumes in template_volumes_dict.values():
            for volume in volumes:
                containers = self.find_containers_for_volume(volume)
                for container in containers:
                    containers_to_add[container] = 1 + containers_to_add.get(
                        container, 0
                    )

        for container, amount in containers_to_add.items():
            values = {
                "order_id": self.id,
                "name": container.name,
                "product_uom_qty": amount,
                "product_uom": container.uom_id.id,
                "product_id": container.id,
                "price_unit": container.lst_price,
                # TODO: tax_id
            }
            line = self.env["sale.order.line"].sudo().create(values)
            total_container_price += line.price_total

        discount = min(total_container_price, self.partner_id.current_deposit)
        deposit_product = self.env[
            "ir.config_parameter"
        ].get_container_deposit_product_id()
        if discount and deposit_product:
            values = {
                "order_id": self.id,
                "name": deposit_product.name,
                "product_uom_qty": 1,
                "product_uom": deposit_product.uom_id.id,
                "product_id": deposit_product.id,
                "price_unit": -discount,
                # TODO: tax_id
            }
            self.env["sale.order.line"].sudo().create(values)

    def _cart_update(
        self, product_id=None, line_id=None, add_qty=0, set_qty=0, **kwargs
    ):
        self._remove_containers()

        values = super()._cart_update(product_id, line_id, add_qty, set_qty, **kwargs)
        return values

    def _remove_containers(self):
        self.ensure_one()
        deposit_product = self.env[
            "ir.config_parameter"
        ].get_container_deposit_product_id()

        lines_to_remove = self.order_line.filtered(
            lambda line: line.product_id.is_container
            or line.product_id == deposit_product
        )
        lines_to_remove.unlink()


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    not_returned = fields.Integer(string="Not Returned", default=0)
    is_container = fields.Boolean(related="product_id.is_container")

    @api.constrains("not_returned", "product_uom_qty")
    def _check_not_returned(self):
        for line in self:
            if line.not_returned != 0 and not line.product_id.is_container:
                raise ValidationError(_("'Not Returned' is only for containers."))
            elif line.not_returned < 0:
                raise ValidationError(_("'Not Returned' must be zero or higher."))
            elif line.not_returned > line.product_uom_qty:
                raise ValidationError(
                    _("'Not Returned' may not be higher than Quantity.")
                )
