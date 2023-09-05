from odoo import _, api, fields, models
from odoo.exceptions import UserError


class DeliveryDistributionList(models.Model):
    _name = "delivery.distribution.list"

    name = fields.Char(string="Name", copy=False)
    distribution_date = fields.Date(
        string="Distribution Date",
        readonly=True,
        required=True,
        index=True,
        states={"draft": [("readonly", False)]},
    )
    create_date = fields.Date(
        string="Creation Date",
        readonly=True,
        help="Date on which distribution list is created.",
        copy=False,
        default=fields.Datetime.now,
    )

    user_id = fields.Many2one(
        "res.users",
        string="Distribution responsible",
        index=True,
        copy=False,
        default=lambda self: self.env.user,
    )
    product_id = fields.Many2one(
        "product.template",
        string="Product",
        domain=[("sale_ok", "=", True)],
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    distribution_lines = fields.One2many(
        "delivery.distribution.line",
        "distribution_list_id",
        string="Distribution lines",
        copy=False,
    )
    journal_id = fields.Many2one(
        "account.journal",
        string="Journal",
        domain=[("type", "=", "sale")],
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
            ("done", "Done"),
            ("cancelled", "Cancelled"),
        ],
        string="State",
        readonly=True,
        copy=False,
        default="draft",
    )

    def action_validate(self):
        self.ensure_one()
        self.distribution_lines.write({"state": "validated"})
        self.state = "validated"

    def action_draft(self):
        self.ensure_one()
        self.distribution_lines.write({"state": "draft"})
        self.state = "draft"

    def action_done(self):
        self.ensure_one()
        self.state = "done"

    def action_sale(self):
        self.ensure_one()
        self.distribution_lines.generate_sale_order()
        self.state = "sale"

    def action_send_sale_order(self):
        self.ensure_one()
        self.distribution_lines.send_sale_order()
        self.state = "sale_sent"

    def action_invoice(self):
        self.ensure_one()
        self.distribution_lines.invoice_sale_order()
        self.state = "invoiced"

    def action_validate_invoice(self):
        self.ensure_one()
        self.distribution_lines.validate_invoice()
        self.state = "invoice_validated"

    def action_send_invoice(self):
        self.ensure_one()
        self.distribution_lines.send_invoice()
        self.state = "invoice_sent"

    def action_cancel(self):
        self.ensure_one()
        self.state = "cancelled"

    def generate_distribution_list(self):
        self.ensure_one()
        deposit_points = self.env["res.partner"].search([("deposit_point", "=", True)])

        # delete existing lines if any
        if self.state == "draft":
            if not self.name:
                ddl_seq = self.env.ref("delivery_distribution_list.sequence_ddl", False)
                self.name = ddl_seq.next_by_id()
            self.distribution_lines.unlink()
            vals = {"distribution_list_id": self.id, "product_id": self.product_id.id}

            for deposit_point in deposit_points:
                if deposit_point.quantity_to_deliver > 0.0:
                    vals["partner_id"] = deposit_point.id
                    vals["carrier_id"] = deposit_point.carrier_id.id
                    vals["ordered_qty"] = deposit_point.quantity_to_deliver
                    vals["delivered_qty"] = deposit_point.quantity_to_deliver
                    self.env["delivery.distribution.line"].create(vals)

    def unlink(self):
        for distri_list in self:
            if distri_list.state != "draft":
                raise UserError(
                    _(
                        "It is forbidden to modify a distribution list which "
                        "is not in draft status"
                    )
                )
            super(DeliveryDistributionList, self).unlink()


class DeliveryDistributionLine(models.Model):
    _name = "delivery.distribution.line"

    _order = "distribution_list_id desc, partner_id, date"

    def _compute_sold_qty(self):
        for line in self:
            line.sold_qty = line.delivered_qty - line.returned_qty

    distribution_list_id = fields.Many2one(
        "delivery.distribution.list", string="Distribution list", required=True
    )
    partner_id = fields.Many2one(
        "res.partner",
        string="Customer",
        domain=[("deposit_point", "=", True)],
        required=True,
    )
    product_id = fields.Many2one("product.template", string="Product", required=True)
    date = fields.Date(
        string="Creation Date",
        readonly=True,
        help="Date on which distribution line is created.",
        default=fields.Datetime.now,
    )
    product_uom = fields.Many2one(
        related="product_id.uom_id", string="Unit of Measure", readonly=True
    )
    ordered_qty = fields.Float(
        string="Quantity Ordered",
        digits="Product Unit of Measure",
        required=True,
    )
    delivered_qty = fields.Float(
        string="Quantity Delivered",
        digits="Product Unit of Measure",
        default=0.0,
        required=True,
    )
    returned_qty = fields.Float(
        string="Quantity Returned",
        digits="Product Unit of Measure",
        default=0.0,
        required=True,
    )
    sold_qty = fields.Float(
        string="Quantity Sold",
        digits="Product Unit of Measure",
        compute="_compute_sold_qty",
    )
    carrier_id = fields.Many2one(
        "res.partner",
        string="Assigned carrier",
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
        string="State",
        readonly=True,
        copy=False,
        index=True,
        default="draft",
    )

    sale_order = fields.Many2one("sale.order", string="Sale Order", readonly=True)

    def unlink(self):
        self.ensure_one()
        if self.state != "draft":
            raise UserError(
                _(
                    "It is forbidden to modify a distribution list which is not in draft status"
                )
            )
        super(DeliveryDistributionLine, self).unlink()

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
        order_line_obj = self.env["sale.order.line"]
        for line in self:
            vals = {
                "partner_id": line.partner_id.id,
                "distribution_list_id": line.distribution_list_id.id,
                "distribution_carrier_id": line.carrier_id.id,
                "project_id": line.product_id.analytic_account_id.id,
            }
            order_id = sale_order_obj.create(vals)
            vals_line = {
                "product_id": line.product_id.id,
                "product_uom_qty": line.delivered_qty,
                "product_uom": line.product_uom.id,
                "order_id": order_id.id,
            }
            order_line_obj.create(vals_line)
            line.sale_order = order_id
            order_id.action_confirm()
            line.state = "sale"

    def send_sale_order(self):
        ir_model_data = self.env["ir.model.data"]
        mail_template_obj = self.env["mail.template"]
        mail_template_id = ir_model_data.get_object_reference(
            "sale", "email_template_edi_sale"
        )[1]
        mail_template = mail_template_obj.browse(mail_template_id)
        for line in self:
            mail_template.send_mail(line.sale_order.id, False)
            line.state = "sale_sent"

    def invoice_sale_order(self):
        for line in self:
            if line.state in ["sale", "sale_sent"]:
                if line.sale_order.invoice_status == "to invoice":
                    line.sale_order.action_invoice_create()
                    line.sale_order.invoice_ids.journal_id = (
                        line.distribution_list_id.journal_id
                    )
                    line.state = "invoiced"

    def validate_invoice(self):
        for line in self:
            if line.state == "invoiced":
                line.sale_order.invoice_ids.signal_workflow("invoice_open")
                line.state = "invoice_validated"

    def send_invoice(self):
        mail_template = self.env.ref("account.email_template_edi_invoice", False)
        for line in self:
            if line.state == "invoice_validated":
                mail_template.send_mail(line.sale_order.invoice_ids.id, False)
                line.state = "invoice_sent"

    @api.onchange("partner_id")
    def onchage_partner_id(self):
        self.delivered_qty = self.partner_id.quantity_to_deliver
        self.ordered_qty = self.partner_id.quantity_to_deliver
        self.carrier_id = self.partner_id.carrier_id.id

    @api.onchange("ordered_qty")
    def onchage_orderer_qty(self):
        self.delivered_qty = self.ordered_qty
