# SPDX-FileCopyrightText: 2023 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from collections import defaultdict

from odoo.http import request
from odoo.tools.translate import _

from odoo.addons.portal.controllers.portal import CustomerPortal


def translate_month(number):
    MONTHS = {
        1: _("January"),
        2: _("February"),
        3: _("March"),
        4: _("April"),
        5: _("May"),
        6: _("June"),
        7: _("July"),
        8: _("August"),
        9: _("September"),
        10: _("October"),
        11: _("November"),
        12: _("December"),
    }
    return MONTHS[number]


def sums_of_years(per_month):
    """Given a dictionary `(year, month): value`, return a dictionary `year:
    new_value`, where `new_value` is the aggregate of all the months for that
    year.
    """
    result = defaultdict(int)
    for key, value in per_month.items():
        result[key[0]] += value
    return dict(result)


class CustomerWalletAmountPortal(CustomerPortal):
    def _prepare_portal_layout_values(self):
        values = super(CustomerWalletAmountPortal, self)._prepare_portal_layout_values()
        user = request.env.user
        partner_id = user.partner_id

        per_month = partner_id.customer_wallet_payments_per_month()
        per_year = sums_of_years(per_month)

        ordered = []
        years = set()
        for key, value in sorted(per_month.items(), reverse=True):
            year = key[0]
            month = key[1]
            if year not in years:
                ordered.append(
                    {
                        "month": str(year),
                        "amount": per_year[year],
                    }
                )
                years.add(year)
            ordered.append(
                {
                    "month": f"{translate_month(month)} {year}",
                    "amount": value,
                }
            )

        values["customer_wallet_payments_per_month"] = ordered
        values["company_currency"] = (
            request.env["res.company"]._company_default_get().currency_id
        )
        values["customer_wallet_balance"] = partner_id.customer_wallet_balance
        return values
