# Part of Open Architechts Consulting sprl. See LICENSE file for full
# copyright and licensing details.

from odoo import api, fields, models


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    _order = "date_planned_start desc,id"  # initially "date_planned_start asc,id"

    # fixme lot_number not used
    lot_number = fields.Many2one("stock.production.lot", string="Lot Number")

    brew_number = fields.Char(string="Brew Number", compute="_compute_brew_number")
    brew_order_name = fields.Char(
        compute="_compute_brew_order_name", String="Brew Order Name"
    )
    brew_orders = fields.One2many(
        "brew.order", "production_order_id", string="Brew Order", readonly=True
    )
    master_mo_id = fields.Many2one(
        "mrp.production",
        domain=[
            ("product_tmpl_id.is_brewable", "=", True),
            ("state", "not in", ["draft", "cancel"]),
        ],
        string="Master production order",
    )
    child_mo_ids = fields.One2many(
        "mrp.production", "master_mo_id", string="Childs production order"
    )

    @api.multi
    @api.depends(
        "master_mo_id",
        "master_mo_id.brew_number",
        "brew_orders.state",
        "brew_orders.brew_number",
        "brew_orders.start_date",
    )
    def _compute_brew_number(self):
        for mo in self:
            if mo.master_mo_id:
                mo.brew_number = mo.master_mo_id.brew_number
            else:
                for brew_order in mo.brew_orders:
                    mo.brew_number = brew_order.brew_number

    @api.multi
    @api.depends(
        "master_mo_id",
        "master_mo_id.brew_number",
        "brew_orders.state",
        "brew_orders.brew_number",
        "brew_orders.start_date",
    )
    def _compute_brew_order_name(self):
        for mo in self:
            if mo.master_mo_id:
                master_mo = mo.master_mo_id
            else:
                master_mo = mo

            if master_mo.brew_orders:
                mo.brew_order_name = master_mo.brew_orders[0].name
            else:
                mo.brew_order_name = "/"

    @api.multi
    def name_get(self):
        res = []
        for record in self:
            if record.origin:
                name = "[{}] {}".format(record.origin, record.name)
            else:
                name = record.name
            res.append((record.id, name))
        return res

    @api.multi
    def open_produce_product(self):
        if not self.product_id.is_brewable and not self.master_mo_id:
            parent_mo = self.search([("name", "=", self.origin)])
            master_mo = False
            while len(parent_mo) > 0:
                master_mo = parent_mo
                parent_mo = self.search([("name", "=", parent_mo.origin)])
            self.write(
                {
                    "brew_number": master_mo.brew_number,
                    "master_mo_id": master_mo.id,
                }
            )
        return super(MrpProduction, self).open_produce_product()
