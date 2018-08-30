# -*- coding: utf-8 -*-
# © 2016 Robin Keunen, Coop IT Easy SCRL fs
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp import models, fields, api


class pos_config(models.Model):
    _inherit = 'pos.config'

    cash_rounding_activated = fields.Boolean(
        string='Activate Cash Rounding',
        default=False,
    )

    round_remainder_product_id = fields.Many2one(
        comodel_name='product.product',
        string='Round Remainder Product',
    )
