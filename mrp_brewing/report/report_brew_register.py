import time

from odoo import _, api, models
from odoo.exceptions import UserError


class ReportBrewRegister(models.AbstractModel):
    _name = "report.mrp_brewing.brew_register"
    _description = "Brew Register Report"

    def get_brew_orders(self, data):
        lines = self.env["brew.order"].search([("state", "=", "done")])
        return lines

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env["brew.order"].browse(self.env.context.get("active_id"))
        report_lines = self.get_brew_orders(data.get("form"))
        return {
            "doc_ids": self.ids,
            "doc_model": "brew.order",
            "data": data.get("form", False),
            "docs": docs,
            "time": time,
            "get_brew_orders": report_lines,
        }
