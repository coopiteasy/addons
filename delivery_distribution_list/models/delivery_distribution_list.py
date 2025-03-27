from odoo import _, fields, models
from odoo.exceptions import UserError


class DeliveryDistributionList(models.Model):
    _name = "delivery.distribution.list"
    _description = "Delivery Distribution List"

    name = fields.Char(copy=False)
    distribution_date = fields.Date(
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
        "product.product",
        string="Product",
        domain=[("sale_ok", "=", True)],
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    distribution_lines = fields.One2many(
        "delivery.distribution.line",
        "distribution_list_id",
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
        if self.state != "draft":
            return
        deposit_points = self.env["res.partner"].search(
            [("deposit_point", "=", True), ("quantity_to_deliver", ">", 0)]
        )
        if not self.name:
            ddl_seq = self.env.ref("delivery_distribution_list.sequence_ddl", False)
            self.name = ddl_seq.next_by_id()
        vals_list = [
            {
                "product_id": self.product_id.id,
                "partner_id": deposit_point.id,
                "carrier_id": deposit_point.carrier_id.id,
                "ordered_qty": deposit_point.quantity_to_deliver,
                "delivered_qty": deposit_point.quantity_to_deliver,
            }
            for deposit_point in deposit_points
        ]
        self.distribution_lines = [fields.Command.clear()] + [
            fields.Command.create(vals) for vals in vals_list
        ]

    def unlink(self):
        for distri_list in self:
            if distri_list.state != "draft":
                raise UserError(
                    _(
                        "It is forbidden to modify a distribution list which "
                        "is not in draft status"
                    )
                )
        return super().unlink()
