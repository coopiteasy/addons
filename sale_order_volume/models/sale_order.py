# -*- coding: utf-8 -*-
# © 2016 Robin Keunen, Coop IT Easy SCRL.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import api, fields, models
from collections import defaultdict


def _compute_volume(order_line):
    return order_line.product_id.volume * order_line.product_uom_qty


class ProductCategoryVolume(models.Model):
    _name = 'product.category.volume'

    sale_order_id = fields.Many2one(
        comodel_name='sale.order',
        string='sale.order',
    )
    category_id = fields.Many2one(
        comodel_name='product.category',
        string='Product Category'
    )
    volume = fields.Float(
        string='Volume (m³)',
    )
    pallet_no = fields.Integer(
        string="Number of pallets",
        compute='compute_pallet_no'
    )

    @api.model
    def get_pallet_volume_indication(self):
        pallet_volume = float(self.env["ir.config_parameter"].get_param(
        'sale_order_volume.pallet_volume'
        )) or 0
        return "One pallet = %.2f m³" % pallet_volume

    @api.depends('volume')
    def compute_pallet_no(self):
        pallet_volume = float(self.env["ir.config_parameter"].get_param(
            'sale_order_volume.pallet_volume'
        ))
        for product in self:
            if pallet_volume:
                product.pallet_no = product.volume // pallet_volume
            else:
                product.pallet_no = 0

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    volume = fields.Float(
        string='Order Volume (m³)',
        compute='compute_order_volume',
        store=True,
    )

    volume_per_category = fields.One2many(
        comodel_name='product.category.volume',
        inverse_name='sale_order_id',
        string='Volume per Product Category',
    )

    @api.multi
    @api.depends('order_line',
                 'order_line.product_id',
                 'order_line.product_uom_qty')
    def compute_order_volume(self):

        for order in self:
            order_lines = order.order_line.filtered(
                lambda ol: ol.state not in ['cancel']
            )

            order.volume = sum(_compute_volume(ol) for ol in order_lines)

    @api.multi
    def compute_order_product_category_volumes(self):
        self.ensure_one()
        CategoryVolume = self.env['product.category.volume']

        order_lines = self.order_line.filtered(
            lambda ol: ol.state not in ['cancel']
        )

        accumulator = defaultdict(list)
        for order_line in order_lines:
            category_id = order_line.product_id.categ_id.id
            volume = _compute_volume(order_line)
            accumulator[category_id].append(volume)

        volume_per_category = [
            (category_id, sum(volumes))
            for category_id, volumes
            in accumulator.items()
        ]

        existing_categories = {
            vpc.category_id.id: vpc for vpc in self.volume_per_category
        }

        for category_id, volume in volume_per_category:
            if category_id in existing_categories:
                existing_categories[category_id].volume = volume
            else:
                vals = {
                    'sale_order_id': self.id,
                    'category_id': category_id,
                    'volume': volume
                }
                CategoryVolume.create(vals)

        return self.volume_per_category

    @api.multi
    def compute_product_category_volumes(self):
        for order in self:
            order.compute_order_product_category_volumes()

    @api.multi
    def write(self, values):
        ret = super(SaleOrder, self).write(values)
        self.compute_product_category_volumes()
        return ret
