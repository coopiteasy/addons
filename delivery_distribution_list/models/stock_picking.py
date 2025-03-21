from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    distribution_carrier_id = fields.Many2one(
        comodel_name="res.partner",
        compute="_compute_distribution_fields",
        string="Assigned carrier",
        store=True,
    )
    distribution_list_id = fields.Many2one(
        comodel_name="delivery.distribution.list",
        compute="_compute_distribution_fields",
        string="Distribution list",
        store=True,
    )

    @api.depends("move_ids")
    def _compute_distribution_fields(self):
        self.distribution_list_id = False
        for picking in self:
            if picking.sale_id:
                picking.distribution_carrier_id = (
                    picking.sale_id.distribution_carrier_id
                )
                picking.distribution_list_id = picking.sale_id.distribution_list_id
