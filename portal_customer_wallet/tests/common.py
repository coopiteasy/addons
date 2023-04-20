# SPDX-FileCopyrightText: 2023 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import datetime

from odoo.tests.common import SavepointCase


class TestCommon(SavepointCase):
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
                "user_type_id": cls.env.ref(
                    "account.data_account_type_current_liabilities"
                ).id,
            }
        )
        cls.company_id.customer_wallet_account_id = cls.customer_wallet_account
        cls.customer_wallet_journal = cls.env["account.journal"].create(
            {
                "name": "Test Wallet Journal",
                "code": "TSTWLLT",
                "type": "bank",
                "is_customer_wallet_journal": True,
                "default_debit_account_id": cls.customer_wallet_account.id,
                "default_credit_account_id": cls.customer_wallet_account.id,
            }
        )
        cls.cash_account = cls.env["account.account"].create(
            {
                "name": "Test Cash Account",
                "code": "654321",
                "user_type_id": cls.env.ref("account.data_account_type_liquidity").id,
            }
        )
        cls.cash_journal = cls.env["account.journal"].create(
            {
                "name": "Test Cash Journal",
                "code": "TSTCASH",
                "type": "cash",
                "journal_user": True,
                "default_debit_account_id": cls.cash_account.id,
                "default_credit_account_id": cls.cash_account.id,
            }
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
                    (
                        0,
                        0,
                        {
                            "debit": debit,
                            "credit": credit,
                            "partner_id": partner.id,
                            "account_id": self.customer_wallet_account.id,
                        },
                    ),
                    (
                        0,
                        0,
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
