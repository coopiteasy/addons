# Part of Open Architechts Consulting sprl. See LICENSE file for full
# copyright and licensing details.

from odoo import api, fields, models


class BrewDeclaration(models.Model):
    _name = "brew.declaration"

    brew_declaration_number = fields.Integer(
        string="Brew declaration number", readonly=True, copy=False
    )
    request_date = fields.Date(string="Request date", required=True)
    state = fields.Selection(
        [("draft", "Draft"), ("confirm", "confirm"), ("cancel", "Cancelled")],
        string="Status",
        readonly=True,
        default="draft",
    )
    brew_orders = fields.One2many(
        "brew.order", "brew_declaration_id", string="Brew Orders"
    )

    @api.multi
    def action_confirm(self):
        brew_declaration_number = self.env["ir.sequence"].next_by_code(
            "brew.declaration.sequence"
        )
        self.write(
            {
                "state": "confirm",
                "brew_declaration_number": int(brew_declaration_number),
            }
        )

    @api.multi
    def action_cancel(self):
        return self.write({"state": "cancel"})

    @api.multi
    def action_draft(self):
        return self.write({"state": "draft"})
