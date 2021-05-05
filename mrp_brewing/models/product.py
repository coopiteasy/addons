#  file for full copyright and licensing details.

from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.multi
    def compute_master_mo_candidates(self):
        self.ensure_one()
        available_lots = (
            self.env["stock.quant"]
            .search(
                [
                    ("product_id", "=", self.id),
                    ("location_id.usage", "=", "internal"),
                ]
            )
            .mapped("lot_id")
            .filtered(lambda l: l.qty_available > 0)
        )

        master_mos = self.env["mrp.production"].search(
            [
                ("origin", "in", available_lots.mapped("name")),
                ("master_mo_id", "=", False),
            ]
        )
        return master_mos


class ProductTemplate(models.Model):
    _inherit = "product.template"

    raw_material = fields.Boolean(string="Is Raw Material")
    finished_product = fields.Boolean(string="Is Finished Product")
    is_brewable = fields.Boolean(string="Is Brewable")
    is_crate = fields.Boolean(string="Is Crate", default=False)
    brew_product_sequence = fields.Many2one(
        "ir.sequence", string="Brew product sequence"
    )


class ProductPricelist(models.Model):
    _inherit = "product.pricelist"

    # TODO: could be moved to a new module `product_pricelist_conditions`
    # that add fields `general_conditions` & `particular_conditions`
    particular_conditions = fields.Text("Particular Conditions")
