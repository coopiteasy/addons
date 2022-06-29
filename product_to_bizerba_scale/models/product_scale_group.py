# Copyright 2014-2017 GRAP (http://www.grap.coop)
#   - Sylvain LE GAL (https://twitter.com/legalsylvain)
# Copyright 2017-Today Coop IT Easy SC
#   - Houssine BAKKALI <houssine@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class ProductScaleGroup(models.Model):
    _name = "product.scale.group"
    _description = "Product Scale Group"

    name = fields.Char(string="Name", required=True)
    active = fields.Boolean(string="Active", default=True)
    external_identity = fields.Char(string="External ID", required=True)
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        default=lambda self: self.env["res.company"]._company_default_get(
            "product.template"
        ),
        index=True,
    )
    scale_system_id = fields.Many2one(
        comodel_name="product.scale.system",
        string="Scale System",
        required=True,
    )
    product_ids = fields.One2many(
        comodel_name="product.template",
        inverse_name="scale_group_id",
        string="Products",
    )
    product_qty = fields.Integer(
        string="Products Quantity", compute="_compute_product_qty"
    )

    @api.multi
    def send_all_to_scale_create(self):
        for scale_group in self:
            (
                scale_group.product_ids.filtered(
                    lambda r: r.is_in_scale()
                ).send_scale_create()
            )

    @api.multi
    def send_all_to_scale_write(self):
        for scale_group in self:
            (
                scale_group.product_ids.filtered(
                    lambda r: r.is_in_scale()
                ).send_scale_write()
            )

    @api.multi
    def send_all_to_scale_unlink(self):
        for scale_group in self:
            scale_group.product_ids.send_scale_unlink()

    @api.multi
    @api.depends("product_ids")
    def _compute_product_qty(self):
        for group in self:
            group.product_qty = len(group.product_ids)
