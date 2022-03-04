# Copyright 2022 Coop IT Easy SCRLfs
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import SavepointCase


class TestDeliveryGrid(SavepointCase):
    def test_new_values_exist(self):
        available_values = (
            self.env["delivery.price.rule"]
            ._fields["variable"]
            .get_values(self.env)
        )

        for choice in ["length", "height", "width"]:
            self.assertIn(choice, available_values)
