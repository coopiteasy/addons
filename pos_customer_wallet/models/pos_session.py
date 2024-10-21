# SPDX-FileCopyrightText: 2023 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import models
from odoo.fields import Command


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

    # This function is called as part of closing the session. We need to add
    # some extra behaviour because, after closing, only a single
    # account.move.line is created against the Customer Wallet account on the
    # Account Receivable (PoS) journal. This is wrong. We need one
    # account.move.line for every partner.
    def _reconcile_account_move_lines(self, data):
        data = super()._reconcile_account_move_lines(data)
        self._reconcile_account_move_lines_customer_wallet(data)
        # This data does not match exactly anymore (some move lines were
        # shuffled). We could theoretically put in the effort to also do the
        # shuffling in the data object, but it's fine for now, because this data
        # doesn't appear to be subsequently used anywhere.
        return data

    def _reconcile_account_move_lines_customer_wallet(self, data):
        sales = data.get("sales")
        # This account.move.line empty recordset has a special context that
        # allows us to make changes that aren't exactly in sync with the
        # account.move. We need this because we'll very temporarily be out of
        # sync in between unlinking the old lines and creating the new ones.
        MoveLine = data.get("MoveLine")

        # We want to remove all account.move.lines with accumulated information
        # across many partners, and create new account.move.lines who have
        # partner_ids. Instead of doing this one-by-one, we create a record of
        # all the stuff we want to change, and then do it in bulk at the end.
        to_unlink = MoveLine.browse()
        to_create = []

        for sale_key, sale_val in sales.items():
            sale_account = self.env["account.account"].browse(sale_key[0])
            # Only work on sales involving the customer wallet. Skip everything
            # else.
            if sale_account != self.env.company.customer_wallet_account_id:
                continue
            account_move_line = self.env["account.move.line"].browse(
                sale_val["move_line_id"]
            )
            account_move = account_move_line.move_id

            to_unlink |= account_move_line

            order_lines = self._search_customer_wallet_order_lines(sale_key)
            for order_line in order_lines:
                price = order_line.price_subtotal
                partner = order_line.order_id.partner_id

                amounts = {"amount": 0, "amount_converted": 0}
                amounts = self._update_amounts(
                    amounts, {"amount": price}, account_move_line.date
                )

                # These vals are similar to _get_sale_vals() in point_of_sale.
                vals = {
                    "name": account_move_line.name,
                    "partner_id": partner.id,
                    "account_id": account_move_line.account_id.id,
                    "move_id": account_move.id,
                    "tax_ids": [Command.set(account_move_line.tax_ids.ids)],
                    "tax_tag_ids": [Command.set(account_move_line.tax_tag_ids.ids)],
                }
                # Add credit/debit stuff.
                vals = self._credit_amounts(
                    vals, amounts["amount"], amounts["amount_converted"]
                )

                to_create.append(vals)

        # Make all changes in bulk.
        moves = self.env["account.move"].search([("line_ids", "in", to_unlink.ids)])
        # Un-post and re-post the account.moves to be able to make changes to
        # them.
        moves.button_draft()
        to_unlink.unlink()
        MoveLine.create(to_create)
        # This validates that we did everything right, too.
        moves.action_post()

    def _search_customer_wallet_order_lines(self, sale_key):
        result = self.env["pos.order.line"]
        for order in self.order_ids.filtered(lambda order: not order.is_invoiced):
            for order_line in order.lines:
                line = self._prepare_line(order_line)
                # Copied from point_of_sale.
                reconstructed_sale_key = (
                    # account
                    line["income_account_id"],
                    # sign
                    -1 if line["amount"] < 0 else 1,
                    # for taxes
                    tuple(
                        (tax["id"], tax["account_id"], tax["tax_repartition_line_id"])
                        for tax in line["taxes"]
                    ),
                    line["base_tags"],
                )
                if sale_key == reconstructed_sale_key:
                    result |= order_line
        return result
