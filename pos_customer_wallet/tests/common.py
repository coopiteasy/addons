# Copyright 2022 Coop IT Easy SC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from random import randint

from odoo import fields

from odoo.addons.account_customer_wallet.tests.common import TestBalance


class TestPosBalance(TestBalance):
    @classmethod
    def setUpClass(cls, *args, **kwargs):
        super().setUpClass(*args, **kwargs)

        cls.customer_wallet_payment_method = cls.env.ref(
            "pos_customer_wallet.customer_wallet_payment_method"
        )

    def _create_random_uid(self):
        return "%05d-%03d-%04d" % (randint(1, 99999), randint(1, 999), randint(1, 9999))

    # TODO: maybe also pass a pos_config or pos_session as parameter. not
    # necessary yet
    def _create_pos_order(self, product, payment_method, amount, partner):
        pricelist = self.env["product.pricelist"].create(
            {
                "name": "Test pricelist",
                "currency_id": self.env.company.currency_id.id,
                "item_ids": [
                    (
                        0,
                        0,
                        {
                            "applied_on": "3_global",
                            "compute_price": "formula",
                            "base": "list_price",
                        },
                    )
                ],
            }
        )
        uid = self._create_random_uid()

        # Create a new pos config and open it
        pos_config = self.env.ref("point_of_sale.pos_config_main").copy(
            {
                "available_pricelist_ids": [(6, 0, pricelist.ids)],
                "pricelist_id": pricelist.id,
            }
        )
        pos_config.payment_method_ids += self.customer_wallet_payment_method
        pos_config.open_ui()
        pos_session = pos_config.current_session_id
        pos_session.action_pos_session_open()
        # Bypass cash control
        pos_session.state = "opened"

        order_data = {
            "data": {
                "name": "Order %s" % uid,
                "amount_paid": amount,
                "amount_total": amount,
                "amount_tax": 0,
                "amount_return": 0,
                "lines": [
                    [
                        0,
                        0,
                        {
                            "qty": 1,
                            "price_unit": amount,
                            "price_subtotal": amount,
                            "price_subtotal_incl": amount,
                            "discount": 0,
                            "product_id": product.id,
                            "tax_ids": [[6, 0, []]],
                            # The randint seems rather strange to me, but I
                            # nicked this idea from tests/common.py in the pos
                            # module.
                            "id": randint(1000, 1000000),
                            "pack_lot_ids": [],
                        },
                    ]
                ],
                "statement_ids": [
                    [
                        0,
                        0,
                        {
                            "name": fields.Datetime.to_string(fields.Datetime.now()),
                            "payment_method_id": payment_method.id,
                            "amount": amount,
                        },
                    ]
                ],
                "pos_session_id": pos_session.id,
                "pricelist_id": pricelist.id,
                "partner_id": partner.id,
                "user_id": self.env.user.id,
                "uid": uid,
                "sequence_number": 1,
                "creation_date": fields.Datetime.to_string(fields.Datetime.now()),
                "fiscal_position_id": False,
                "to_invoice": False,
            },
            "uid": uid,
            "to_invoice": False,
        }

        return self.env["pos.order"].create_from_ui([order_data])

    def _create_wallet_pos_payment(self, amount=0, partner=None):
        if partner is None:
            partner = self.partner
        self._create_pos_order(
            self.env["product.product"].create(
                {
                    "name": "Foo Product",
                    "available_in_pos": True,
                    "list_price": amount,
                    "taxes_id": False,
                }
            ),
            self.customer_wallet_payment_method,
            amount,
            partner,
        )
