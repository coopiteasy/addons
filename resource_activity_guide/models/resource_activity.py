# Copyright 2021 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


from openerp import api, fields, models
from openerp.addons.resource_activity.models.resource_activity import OrderLine


class ResourceActivity(models.Model):
    _inherit = "resource.activity"

    need_guide = fields.Boolean(string="Need guide?")
    guide_product_id = fields.Many2one(
        "product.product",
        string="Product Guide",
        domain=[("is_guide", "=", True)],
    )
    comment = fields.Html(string="Guide Comment")
    guides = fields.Many2many(
        "res.partner",
        relation="activity_guide",
        column1="activity_id",
        column2="guide_id",
        string="Guide",
        domain=[("is_guide", "=", True)],
    )

    @api.multi
    def write(self, vals):
        for activity in self:
            if activity.sale_orders:
                if "need_guide" in vals and not vals.get("need_guide"):
                    # reset guide fields
                    vals["guide_product_id"] = False
                    vals["guides"] = [[6, False, []]]

                # if sale order was generated and these values
                #   are updated, the sale order is flagged as
                #   "need push to sale order"
                watches = (
                    "need_guide",
                    "guide_product_id",
                    "guides",
                )
                if any(map(lambda var: var in vals, watches)):
                    vals["need_push"] = True
        return super(ResourceActivity, self).write(vals)

    def _create_order_line(self, order, line_type, product, qty):
        order_line = super(ResourceActivity, self)._create_order_line(
            order, line_type, product, qty
        )
        if line_type == "guide":
            order_line.resource_guide = True
        return order_line

    def _prepare_lines(self):
        prepared_lines = super(ResourceActivity, self)._prepare_lines()
        if self.need_guide and self.partner_id:
            prepared_lines.append(
                OrderLine(
                    self.partner_id.id,
                    self.guide_product_id,
                    len(self.guides),
                    "guide",
                    None,
                )
            )
        return prepared_lines

    # fixme not used ??
    # def update_guide_line(self, activity, sale_order_id):
    #     guide_line = activity.sale_order_id.order_line.filtered(
    #         lambda record: record.resource_guide == True
    #     )
    #     line_vals = {"resource_guide": True}
    #     guide_qty = len(activity.guides)
    #
    #     self.update_order_line(
    #         sale_order_id,
    #         activity.need_guide,
    #         line_vals,
    #         guide_line,
    #         guide_qty,
    #         activity.guide_product_id,
    #     )
