# -*- coding: utf-8 -*-
# © 2016 Robin Keunen, Coop IT Easy SCRL fs
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp import models, fields, api


class pos_config(models.Model):
    _inherit = 'pos.config'

    round_remainder_product_id = fields.Many2one(
        comodel_name='product.product',
        string='Round Remainder Product',
        store=True,
        compute='set_round_remainder_account'
    )

    round_remainder_income_account_id = fields.Many2one(
        comodel_name='account.account',
        string='Round Remainder Income Account',
    )

    round_remainder_expense_account_id = fields.Many2one(
        comodel_name='account.account',
        string='Round Remainder Expense Account',
    )

    @api.depends('round_remainder_income_account_id',
                 'round_remainder_expense_account_id')
    def set_round_remainder_account(self):
        self.ensure_one()
        res_model, res_id = (
            self.env['ir.model.data']
                .get_object_reference('pos_round_cash_payment_line',
                                      'round_remainder_product')
        )
        product = self.env[res_model].browse(res_id)

        product.property_account_income_id = self.round_remainder_income_account_id
        product.property_account_expense_id = self.round_remainder_expense_account_id
        self.round_remainder_product_id = product
