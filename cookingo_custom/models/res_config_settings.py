# Copyright 2022 Coop IT Easy SCRL fs
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    container_deposit_product_id = fields.Many2one(
        'product.product',
        'Container Deposit Product',
        domain="[('type', '=', 'service')]",
        config_parameter='cookingo_custom.container_deposit_product_id',
        help='Product used as deposit for containers')
