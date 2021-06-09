# Copyright 2021 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


from openerp import api, fields, models, _
from openerp.exceptions import ValidationError


class StockRemovalWizard(models.TransientModel):
    _name = "resource.stock.removal.wizard"
    _description = "Resource Stock Removal Wizard"

    resource_id = fields.Many2one(
        comodel_name="resource.resource",
        string="Resource",
        required=True,
    )
    stock_removal_date = fields.Date(
        string="Stock Removal Date", default=lambda _: fields.Date.today()
    )
    stock_removal_reason = fields.Selection(
        string="Stock Removal Reason",
        selection=[
            ("sold", "Sold"),
            ("stolen", "Stolen"),
            ("given", "Given"),
            ("broken", "Broken"),
            ("other", "Other"),
        ],
    )
    selling_price = fields.Float(string="Selling Price")
    sale_invoice_ref = fields.Char(string="Sale Invoice Ref")

    @api.multi
    def remove_resource_from_stock(self):
        self.ensure_one()

        if not self.stock_removal_reason:
            raise ValidationError(
                _(
                    "Please provide a reason for the resource removal from stock"
                )
            )

        self.resource_id.write(
            {
                "removed_from_stock": True,
                "state": "unavailable",
                "stock_removal_date": self.stock_removal_date,
                "stock_removal_reason": self.stock_removal_reason,
                "selling_price": self.selling_price,
                "sale_invoice_ref": self.sale_invoice_ref,
            }
        )
        return
