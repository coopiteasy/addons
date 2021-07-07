from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    pallet_volume = fields.Float(
        string="Pallet Volume (m³)",
        help="Pallet Volume in cubic meter",
        config_parameter="sale_order_volume.pallet_volume",
        digits=(3, 2),
    )
