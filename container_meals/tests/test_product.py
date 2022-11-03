# Copyright 2022 Coop IT Easy SC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from ..models.product import CHILD_PORTION_RATIO
from . import common


class TestProduct(common.TestCommon):
    def test_container_volume_smaller_for_children(self):
        """A child portion's container volume is not as big as an
        adult portion.
        """
        self.assertAlmostEqual(
            self.salad_template.container_1_volume * CHILD_PORTION_RATIO,
            self.salad_product_child.container_1_volume,
        )
        self.assertAlmostEqual(
            self.salad_template.container_2_volume * CHILD_PORTION_RATIO,
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
