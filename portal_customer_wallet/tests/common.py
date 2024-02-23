# SPDX-FileCopyrightText: 2023 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import datetime

from odoo import fields
from odoo.tests.common import TransactionCase


class TestCommon(TransactionCase):
    @classmethod
    def setUpClass(cls, *args, **kwargs):
        super().setUpClass(*args, **kwargs)

        cls.partner_id = cls.env["res.partner"].create({"name": "Test Partner"})
        cls.company_id = cls.env.ref("base.main_company")
        cls.pricelist_id = cls.partner_id.property_product_pricelist
        cls.customer_wallet_account = cls.env["account.account"].create(
            {
                "name": "Test Wallet Account",
                "code": "10101010101",
                "account_type": "liability_current",
            }
        )
        cls.company_id.customer_wallet_account_id = cls.customer_wallet_account
        cls.customer_wallet_journal = cls.env["account.journal"].create(
            {
                "name": "Test Wallet Journal",
                "code": "TSTWLLT",
                "type": "bank",
                "is_customer_wallet_journal": True,
            }
        )
        cls.customer_wallet_journal.inbound_payment_method_line_ids.payment_account_id = (
            cls.customer_wallet_account
        )
        cls.customer_wallet_journal.outbound_payment_method_line_ids.payment_account_id = (
            cls.customer_wallet_account
        )
        cls.cash_account = cls.env["account.account"].create(
            {
                "name": "Test Cash Account",
                "code": "654321",
                "account_type": "asset_cash",
            }
        )
        cls.cash_journal = cls.env["account.journal"].create(
            {
                "name": "Test Cash Journal",
                "code": "TSTCASH",
                "type": "cash",
            }
        )
        cls.cash_journal.inbound_payment_method_line_ids.payment_account_id = (
            cls.cash_account
        )
        cls.cash_journal.outbound_payment_method_line_ids.payment_account_id = (
            cls.cash_account
        )

    def _create_move(self, debit=0, credit=0, date=None, partner=None):
        if partner is None:
            partner = self.partner_id
        if date is None:
            date = datetime.date.today()

        self.env["account.move"].create(
            {
                "journal_id": self.customer_wallet_journal.id,
                "date": date,
                "line_ids": [
                    fields.Command.create(
                        {
                            "debit": debit,
                            "credit": credit,
                            "partner_id": partner.id,
                            "account_id": self.customer_wallet_account.id,
                        },
                    ),
                    fields.Command.create(
                        {
                            "debit": credit,
                            "credit": debit,
                            "partner_id": partner.id,
                            "account_id": self.cash_account.id,
                        },
                    ),
                ],
            }
        )
