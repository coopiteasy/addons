# SPDX-FileCopyrightText: 2023 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo.http import route

from odoo.addons.portal.controllers.portal import CustomerPortal


class SolidarityPortal(CustomerPortal):
    def __init__(self, *args, **kwargs):
        super().__init__()
        if "OPTIONAL_BILLING_FIELDS" not in vars(self):
            self.OPTIONAL_BILLING_FIELDS = CustomerPortal.OPTIONAL_BILLING_FIELDS.copy()
        self.OPTIONAL_BILLING_FIELDS.extend(["enable_solidarity_rounding"])

    @route(["/my/account"], type="http", auth="user", website=True)
    def account(self, redirect=None, **post):
        # When the user sets this to 'off', it doesn't show up in `post`, so
        # let's add it.
        rounding = post.get("enable_solidarity_rounding", False)
        post["enable_solidarity_rounding"] = bool(rounding)
        return super().account(redirect, **post)
