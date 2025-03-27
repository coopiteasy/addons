from odoo import _, api, fields, models
from odoo.exceptions import UserError


class DeliveryDistributionLine(models.Model):
    _name = "delivery.distribution.line"
    _description = "Delivery Distribution Line"

    _order = "distribution_list_id desc, partner_id, date"

    @api.depends("delivered_qty", "returned_qty")
    def _compute_sold_qty(self):
        for line in self:
            line.sold_qty = line.delivered_qty - line.returned_qty

    distribution_list_id = fields.Many2one(
        "delivery.distribution.list",
        string="Distribution List",
        required=True,
        ondelete="cascade",
    )
    partner_id = fields.Many2one(
        "res.partner",
        string="Customer",
        domain=[("deposit_point", "=", True)],
        required=True,
    )
    product_id = fields.Many2one("product.product", string="Product", required=True)
    date = fields.Date(
        readonly=True,
        help="Date on which the distribution line is created",
        default=fields.Datetime.now,
    )
    product_uom = fields.Many2one(
        related="product_id.uom_id", string="Unit of Measure", readonly=True
    )
    ordered_qty = fields.Float(
        string="Ordered",
        digits="Product Unit of Measure",
        required=True,
    )
    delivered_qty = fields.Float(
        string="Delivered",
        digits="Product Unit of Measure",
        default=0.0,
        required=True,
    )
    returned_qty = fields.Float(
        string="Returned",
        digits="Product Unit of Measure",
        default=0.0,
        required=True,
    )
    sold_qty = fields.Float(
        string="Sold",
        digits="Product Unit of Measure",
        compute="_compute_sold_qty",
    )
    carrier_id = fields.Many2one(
        "res.partner",
        string="Carrier",
        domain=[("carrier_delivery", "=", True)],
        readonly=True,
        required=True,
    )

    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("validated", "Validated"),
            ("sale", "Sale Order"),
            ("sale_sent", "Sale order sent"),
            ("invoiced", "Invoiced"),
            ("invoice_validated", "Invoice validated"),
            ("invoice_sent", "Invoice sent"),
            ("cancelled", "Cancelled"),
        ],
        readonly=True,
        copy=False,
        index=True,
        default="draft",
    )

    sale_order = fields.Many2one("sale.order", readonly=True)

    def unlink(self):
        for rec in self:
            if rec.state != "draft":
                raise UserError(
                    _(
                        "It is forbidden to modify a distribution line which "
                        "is not in draft status"
                    )
                )
        return super().unlink()

    def action_validate(self):
        for line in self:
            if line.state == "draft":
                line.state = "validated"

    def action_draft(self):
        for line in self:
            if line.state == "validated":
                line.state = "draft"

    def generate_sale_order(self):
        sale_order_obj = self.env["sale.order"]
        for line in self:
            vals = {
                "partner_id": line.partner_id.id,
                "distribution_list_id": line.distribution_list_id.id,
                "distribution_carrier_id": line.carrier_id.id,
                "order_line": [
                    fields.Command.create(
                        {
                            "product_id": line.product_id.id,
                            "product_uom_qty": line.delivered_qty,
                            "product_uom": line.product_uom.id,
                        }
                    )
                ],
            }
            order_id = sale_order_obj.create(vals)
            line.sale_order = order_id
            order_id.action_confirm()
            line.state = "sale"

    def send_sale_order(self):
        for line in self:
            line.sale_order._send_order_confirmation_mail()
            line.state = "sale_sent"

    def _validate_pickings(self):
        self.ensure_one()
        for picking in self.sale_order.picking_ids:
            if picking.origin != self.sale_order.name or picking.state in [
                "cancel",
                "done",
            ]:
                continue
            if picking.state != "assigned":
                picking.action_assign()
                if picking.state != "assigned":
                    raise UserError(
                        _(
                            "Not enough stock to deliver! Please check that "
                            "there are enough products available."
                        )
                    )
            for move in picking.move_ids:
                if move.product_id != self.product_id:
                    continue
                move.quantity_done = self.sold_qty
                if self.sold_qty < self.delivered_qty:
                    move.product_uom_qty = self.sold_qty
            picking.button_validate()

    def invoice_sale_order(self):
        for line in self:
            if line.state not in ["sale", "sale_sent"]:
                continue
            line._validate_pickings()
            if line.sale_order.invoice_status == "to invoice":
                line.sale_order._create_invoices()
                line.sale_order.invoice_ids.journal_id = (
                    line.distribution_list_id.journal_id
                )
                line.state = "invoiced"

    def validate_invoice(self):
        for line in self:
            if line.state == "invoiced":
                line.sale_order.invoice_ids.action_post()
                line.state = "invoice_validated"

    def send_invoice(self):
        mail_template = self.env.ref("account.email_template_edi_invoice", False)
        for line in self:
            if line.state == "invoice_validated":
                mail_template.send_mail(line.sale_order.invoice_ids.id, False)
                line.state = "invoice_sent"

    @api.onchange("partner_id")
    def _onchange_partner_id(self):
        self.delivered_qty = self.partner_id.quantity_to_deliver
        self.ordered_qty = self.partner_id.quantity_to_deliver
        self.carrier_id = self.partner_id.carrier_id.id

    @api.onchange("ordered_qty")
    def _onchange_orderer_qty(self):
        self.delivered_qty = self.ordered_qty
