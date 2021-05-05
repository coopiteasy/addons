# Part of Open Architechts Consulting sprl. See LICENSE file for full
# copyright and licensing details.

from datetime import date, datetime

from odoo import _, api, fields, models
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError


class BrewOrder(models.Model):
    _name = "brew.order"
    _description = "Brew Order"

    name = fields.Char(
        string="Brew order",
        compute="_compute_name",
        store=True,
        copy=False,
    )
    get_brew_number = fields.Boolean(string="Get brew number ?", default=True)
    brew_number = fields.Char(string="Brew number", copy=False)
    brew_beer_number = fields.Integer(string="Brew beer number", copy=False)
    state = fields.Selection(
        [("draft", "Draft"), ("done", "Done"), ("cancel", "Cancelled")],
        string="Status",
        readonly=True,
        default="draft",
    )
    brew_declaration_id = fields.Many2one(
        "brew.declaration", string="Brew declaration"
    )
    start_date = fields.Datetime(string="Planned date", required=True)
    wort_gathering_date = fields.Datetime(
        string="Wort gathering date", required=True
    )
    end_date = fields.Datetime(string="End date", required=True)
    product_id = fields.Many2one(
        "product.product",
        string="Beer",
        domain=[("is_brewable", "=", True)],
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    product_qty = fields.Float(
        "Product Quantity",
        digits=dp.get_precision("Product Unit of Measure"),
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    product_uom_id = fields.Many2one(
        "uom.uom",
        "Product Unit of Measure",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    production_order_id = fields.Many2one(
        "mrp.production", string="Production Order", readonly=True
    )
    consumed_lines = fields.One2many(
        "stock.move", string="Consumed lines", compute="_compute_consumed_lines"
    )
    bom = fields.Many2one(
        "mrp.bom", string="Bill of material", compute="_compute_bom"
    )
    parent_brew_order_id = fields.Many2one(
        "brew.order", string="parent brew order"
    )
    child_brew_orders = fields.One2many(
        "brew.order", "parent_brew_order_id", string="Child brew order"
    )
    used_vessels_tank = fields.Char(string="Used vessels for work in tank")
    dry_extract = fields.Float(string="% dry extract")
    real_bulk_wort = fields.Float(string="Real bulk of wort")
    hl_plato_brewer = fields.Float(string="Hl plato noted by the brewer")
    hl_plato_agent = fields.Float(string="Hl plato noted by the agents")
    collecting_vessels = fields.Char(string="Collecting vessels")
    green_beer_volume = fields.Float(string="Volume of green Beer")
    sugar_quantity = fields.Float(string="Sugar")
    output_wort = fields.Float(string="Output wort")
    output_beer = fields.Float(string="Output beer")
    notes = fields.Char(string="Notes")

    @api.onchange("product_id")
    def onchange_product(self):
        if self.product_id:
            self.product_uom_id = self.product_id.uom_id

    @api.onchange("start_date")
    def onchange_start_date(self):
        if self.start_date:
            self.end_date = self.start_date
            self.wort_gathering_date = self.start_date

    @api.onchange("end_date")
    def onchange_end_date(self):
        if self.end_date:
            self.wort_gathering_date = self.end_date

    @api.multi
    @api.depends("production_order_id")
    def _compute_consumed_lines(self):
        self.ensure_one()
        for brew_order in self:
            raw_mat_moves = self.env["stock.move"]
            for child_mo in brew_order.production_order_id.child_mo_ids:
                raw_mat_moves |= child_mo.move_raw_ids.filtered(
                    lambda record: record.state == "done"
                )

            raw_mat_moves |= brew_order.production_order_id.move_raw_ids.filtered(
                lambda record: record.state == "done"
            )
            brew_order.consumed_lines = raw_mat_moves

    @api.multi
    @api.depends(
        "product_id", "brew_number", "brew_beer_number", "state", "start_date"
    )
    def _compute_name(self):
        year = date.today().year
        if self.start_date:
            year = self.start_date.year
        for order in self:
            if order.state in ["done", "cancel"]:
                order.name = "{}_{}_{}".format(
                    order.product_id.code, year, order.brew_beer_number,
                )
            else:
                order.name = "{}_{}_{}".format(
                    order.product_id.code, year, order.state,
                )

    @api.multi
    def _compute_bom(self):
        for brew_order in self:
            brew_order.bom = brew_order.production_order_id.bom_id

    @api.multi
    def action_confirm(self):
        bom_id = self.env["mrp.bom"]._bom_find(product=self.product_id)
        if not bom_id:
            raise UserError(
                _("No Bill of Materials found.")
            )
        if self.parent_brew_order_id:
            if self.parent_brew_order_id.state != "done":
                raise UserError(
                    _("You must first confirm the parent brew order.")
                )
        else:
            brew_beer_number = (
                self.product_id.brew_product_sequence.next_by_id()
            )
            brew_year_sequence = self.env["ir.sequence"].search(
                [("code", "=", "brew.year.sequence")]
            )
            brew_year_number = 0
            if self.get_brew_number:
                brew_year_number = brew_year_sequence.next_by_id()
        self.write(
            {
                "state": "done",
                "brew_number": brew_year_number,
                "brew_beer_number": brew_beer_number,
            }
        )

        # create production order
        vals = {
            "product_id": self.product_id.id,
            "product_qty": self.product_qty,
            "product_uom_id": self.product_uom_id.id,
            "date_planned_start": self.start_date,
            "origin": self.name,
            "bom_id": bom_id.id,
        }

        prod_order_id = self.env["mrp.production"].create(vals)
        self.write({"production_order_id": prod_order_id.id})

    @api.multi
    def action_cancel(self):
        return self.write({"state": "cancel"})

    @api.multi
    def action_draft(self):
        return self.write({"state": "draft"})
