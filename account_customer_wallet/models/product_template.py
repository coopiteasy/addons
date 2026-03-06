# Copyright (C) 2022-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_customer_wallet_product = fields.Boolean(
        string="Wallet Product",
        help="Check this box if this product is used to credit" " customer wallets.",
    )

    def _get_product_accounts(self):
        if self.is_customer_wallet_product:
            company = self.company_id or self.env.company
            return {
                "income": company.customer_wallet_account_id,
                "expense": company.customer_wallet_account_id,
            }
        return super()._get_product_accounts()
