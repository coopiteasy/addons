import time

from odoo import _, api, models
from odoo.exceptions import UserError


class ReportRawMaterials(models.AbstractModel):
    _name = "report.mrp_brewing.stock_raw_materials"
    _description = "Stock Raw Materials Report"

    def get_stock_moves(self, data):
        lines = self.env["stock.move"].search(
            [("state", "=", "done"), ("product_id.raw_material", "=", True)],
            order="date asc",
        )

        return lines

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env["stock.move"].browse(self.env.context.get("active_id"))
        report_lines = self.get_stock_moves(data.get("form"))
        return {
            "doc_ids": self.ids,
            "doc_model": "stock.move",
            "data": data.get("form", False),
            "docs": docs,
            "time": time,
            "get_stock_moves": report_lines,
        }
