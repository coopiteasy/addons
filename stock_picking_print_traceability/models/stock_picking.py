from odoo import api, fields, models


class Picking(models.Model):
    _inherit = "stock.picking"

    print_date = fields.Datetime(
        string="Print Date",
        readonly=True,
        help="Date on which stock picking is printed.",
    )

    @api.multi
    def do_print_picking(self):
        """Handles 'Print' button."""
        res = super(Picking, self).do_print_picking()
        self.set_printed(fields.Datetime.now())
        return res

    @api.multi
    def set_printed(self, date):
        self.ensure_one()
        self.write({"printed": True, "print_date": date})  # `printed`: standard field

    @api.multi
    def write(self, vals):
        if "printed" not in vals:
            vals["printed"] = False
        return super().write(vals)
