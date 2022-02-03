# Copyright 2022 Coop IT Easy SCRL fs
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestProduct(TransactionCase):
    def setUp(self, *args, **kwargs):
        result = super().setUp(*args, **kwargs)

        self.attribute_portion_size = self.env.ref(
            "cookingo_custom.product_attribute_portion_size"
        )
        self.attribute_portion_size_adult = self.env.ref(
            "cookingo_custom.product_attribute_portion_size_value_adult"
        )
        self.attribute_portion_size_child = self.env.ref(
            "cookingo_custom.product_attribute_portion_size_value_child"
        )

        # fmt: off
        self.salad_template = self.env["product.template"].create({
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
                    "attribute_id": self.attribute_portion_size.id,
                    "value_ids": [(
                        6,
                        0,
                        [
                            self.attribute_portion_size_adult.id,
                            self.attribute_portion_size_child.id,
                        ],
                    )],
                },
            )],
        })
        # fmt: on

        products = self.env["product.product"].search(
            [
                ("product_tmpl_id", "=", self.salad_template.id),
            ]
        )

        # This is hacky and stupid, and there is doubtlessly a
        # better way.
        for product in products:
            # There should only be one value, but looping anyway.
            for value in product.product_template_attribute_value_ids:
                if value.name == self.attribute_portion_size_adult.name:
                    self.salad_product_adult = product
                else:
                    self.salad_product_child = product

        return result

    def test_container_volume_smaller_for_children(self):
        """A child portion's container volume is 2/3 as big as an
        adult portion.
        """
        self.assertAlmostEqual(
            self.salad_template.container_1_volume * (2 / 3),
            self.salad_product_child.container_1_volume,
        )
        self.assertAlmostEqual(
            self.salad_template.container_2_volume * (2 / 3),
            self.salad_product_child.container_2_volume,
        )

    def test_container_volume_identical_for_adults(self):
        """Adult portions are equally as big as declared in the
        template.
        """
        self.assertAlmostEqual(
            self.salad_template.container_1_volume,
            self.salad_product_adult.container_1_volume,
        )
        self.assertAlmostEqual(
            self.salad_template.container_2_volume,
            self.salad_product_adult.container_2_volume,
        )
