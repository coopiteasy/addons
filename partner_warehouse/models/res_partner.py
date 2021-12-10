from odoo import fields, models


class Partner(models.Model):
    _inherit = "res.partner"

    warehouse_id = fields.Many2one("stock.warehouse", "Warehouse")
