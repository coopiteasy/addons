# Copyright 2022 Coop IT Easy SCRL fs
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from collections import namedtuple

from odoo import api, fields, models

ContainerVolumes = namedtuple(
    "ContainerVolumes", ["container_1_volume", "container_2_volume"]
)
_EMPTY = ContainerVolumes(0, 0)


class SaleOrder(models.Model):
    _inherit = "sale.order"

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
        templates = self.env["product.template"]
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

    def find_containers_for_template(self, template_id, volumes_tuple):
        """Given a template, find container 1 and container 2 that
        will hold the combined volumes of all products belonging to that
        template.

        Example: Elaborating on the example from 'calculate_volume_containers',
        return ``(container that is big enough to hold 900*2+600, container that
        is big enough to hold 600*2+400)``.
        """
        self.ensure_one()
        containers = (
            self.env["product.template"]
            .search([("is_container", "=", True)])
            .sorted(key="container_volume")
        )
        container_1 = None
        container_2 = None
        for container in containers:
            if not container_1 and container.container_volume >= volumes_tuple[0]:
                container_1 = container.product_variant_id
            if not container_2 and container.container_volume >= volumes_tuple[1]:
                container_2 = container.product_variant_id
        # TODO: This may return None if no container is big enough!
        return (container_1, container_2)

    def _cart_update(
        self, product_id=None, line_id=None, add_qty=0, set_qty=0, **kwargs
    ):
        values = super()._cart_update(product_id, line_id, add_qty, set_qty, **kwargs)
        if not self.env["product.product"].browse(product_id).is_meal:
            return values

        template_volumes_dict = self.calculate_volume_containers()
        lines_to_remove = self.order_line.filtered(
            lambda line: line.product_id.is_container
        )
        containers_to_add = {}  # container: amount

        for line in lines_to_remove:
            self._cart_update(
                line.product_id.id, line.id, add_qty=0, set_qty=-1, **kwargs
            )

        for template, volumes in template_volumes_dict.items():
            containers = self.find_containers_for_template(template, volumes)
            for container in containers:
                containers_to_add[container] = 1 + containers_to_add.get(container, 0)

        for container, amount in containers_to_add.items():
            self._cart_update(container.id, None, add_qty=0, set_qty=amount, **kwargs)

        return values
