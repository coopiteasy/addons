# SPDX-FileCopyrightText: 2023 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import models


class PosSession(models.Model):
    _inherit = "pos.session"

    def _loader_params_pos_payment_method(self):
        result = super()._loader_params_pos_payment_method()
        result["search_params"]["fields"].append("is_customer_wallet_method")
        return result

    def _loader_params_product_product(self):
        result = super()._loader_params_product_product()
        result["search_params"]["fields"].append("is_customer_wallet_product")
        return result

    def _loader_params_res_partner(self):
        result = super()._loader_params_res_partner()
        result["search_params"]["fields"].append("customer_wallet_balance")
        return result
