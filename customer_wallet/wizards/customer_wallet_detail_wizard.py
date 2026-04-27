# Copyright (C) 2022-Today: GRAP (http://www.grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# flake8: noqa

from odoo import _, api, fields, models
from odoo.tools import format_amount
from odoo.tools.safe_eval import datetime, safe_eval


class CustomerWalletDetailWizard(models.TransientModel):
    _name = "customer.wallet.detail.wizard"
    _description = "Customer Wallet Detail Wizard"

    partner_id = fields.Many2one(required=True, comodel_name="res.partner")
    currency_id = fields.Many2one(
        comodel_name="res.currency", related="partner_id.currency_id"
    )
    customer_wallet_balance = fields.Monetary(
        related="partner_id.customer_wallet_balance",
        string="Balance",
    )
    customer_wallet_data = fields.Text(related="partner_id.customer_wallet_data")
    detail = fields.Html(compute="_compute_detail_html", sanitize=False)

    @api.depends("partner_id")
    def _compute_detail_html(self):
        for wizard in self.filtered(lambda x: not x.partner_id):
            wizard.detail = False
        for wizard in self.filtered(lambda x: x.partner_id):

            lines = safe_eval(self.customer_wallet_data, {"datetime": datetime})
            lines.sort(key=lambda x: (x["datetime"], x["create_date"]), reverse=True)

            line_details = ""
            for line in lines:
                line_details += f"""
                    <tr>
                        <td>{line["datetime"]}</td>
                        <td>{format_amount(self.env, line["amount"], self.currency_id)}</td>
                        <td>{format_amount(self.env, line["balance"], self.currency_id)}</td>
                        <td>{line["reference"]}</td>
                    </tr>

                """

            if line_details:
                line_details = f"""<tbody>
                        {line_details}
                    </tbody>
                """

            wizard.detail = """
            <div class="o_list_renderer">
                <table class="table table-hover o_list_table">
                    <thead>
                        <tr>
                            <th>{date}</th>
                            <th>{amount}</th>
                            <th>{balance}</th>
                            <th>{reference}</th>
                        </tr>
                    </thead>
                    {line_details}
                </table>
            </div>
            """.format(
                date=_("Date"),
                amount=_("Amount"),
                balance=_("Balance"),
                reference=_("Reference"),
                line_details=line_details,
            )
