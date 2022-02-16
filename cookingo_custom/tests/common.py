# Copyright 2022 Coop IT Easy SCRL fs
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import SavepointCase


class TestCommon(SavepointCase):
    @classmethod
    def setUpClass(cls, *args, **kwargs):
        super().setUpClass(*args, **kwargs)

        cls.attribute_portion_size = cls.env.ref(
            "cookingo_custom.product_attribute_portion_size"
        )
        cls.attribute_portion_size_adult = cls.env.ref(
            "cookingo_custom.product_attribute_portion_size_value_adult"
        )
        cls.attribute_portion_size_child = cls.env.ref(
            "cookingo_custom.product_attribute_portion_size_value_child"
        )

        # fmt: off
        cls.salad_template = cls.env["product.template"].create({
            "name": "Salad",
            "type": "consu",
            "list_price": 12,
            "is_meal": True,
            "container_1_volume": 600,
            "container_2_volume": 300,
            "attribute_line_ids": [(
                0,
                0,
                {
                    "attribute_id": cls.attribute_portion_size.id,
                    "value_ids": [(
                        6,
                        0,
                        [
                            cls.attribute_portion_size_adult.id,
                            cls.attribute_portion_size_child.id,
                        ],
                    )],
                },
            )],
        })
        # fmt: on

        products = cls.env["product.product"].search(
            [
                ("product_tmpl_id", "=", cls.salad_template.id),
            ]
        )

        # This is hacky and stupid, and there is doubtlessly a
        # better way.
        for product in products:
            # There should only be one value, but looping anyway.
            for value in product.product_template_attribute_value_ids:
                if value.name == cls.attribute_portion_size_adult.name:
                    cls.salad_product_adult = product
                else:
                    cls.salad_product_child = product

        cls.container_volumes = (400, 600, 1000, 1200, 1800, 3100)
        cls.containers = {
            key: cls.env["product.template"].create(
                {
                    "name": f"Container {key} mL",
                    "list_price": key / 100,
                    "is_container": True,
                    "container_volume": key,
                    "taxes_id": None,
                }
            )
            for key in cls.container_volumes
        }

        container_deposit_product_template = cls.env["product.template"].create(
            {
                "name": "Deposit",
                "list_price": 0,
                "taxes_id": None,
            }
        )
        cls.container_deposit_product = (
            container_deposit_product_template.product_variant_id
        )
        cls.env["ir.config_parameter"].sudo().set_param(
            "cookingo_custom.container_deposit_product_id",
            cls.container_deposit_product.id,
        )


class TestCommonSaleOrder(TestCommon):
    @classmethod
    def setUpClass(cls, *args, **kwargs):
        super().setUpClass(*args, **kwargs)

        cls.pricelist = cls.env["product.pricelist"].create(
            {"name": "Default Pricelist"}
        )
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Customer",
            }
        )

        cls.sale_order = cls.env["sale.order"].create(
            {
                "name": "Sale",
                "partner_id": cls.partner.id,
                "partner_invoice_id": cls.partner.id,
                "partner_shipping_id": cls.partner.id,
                "pricelist_id": cls.pricelist.id,
            }
        )


class TestCommonDeposit(TestCommonSaleOrder):
    @classmethod
    def setUpClass(cls, *args, **kwargs):
        super().setUpClass(*args, **kwargs)

        cls.previous_sale_order = cls.env["sale.order"].create(
            {
                "name": "Previous Sale",
                "partner_id": cls.partner.id,
                "partner_invoice_id": cls.partner.id,
                "partner_shipping_id": cls.partner.id,
                "pricelist_id": cls.pricelist.id,
            }
        )

        cls.previous_sale_order._cart_update(
            product_id=cls.salad_product_adult.id, line_id=None, add_qty=1, set_qty=0
        )
        cls.previous_sale_order.add_containers()
        cls.previous_sale_order.action_done()
