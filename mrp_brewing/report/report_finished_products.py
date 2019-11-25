# -*- coding: utf-8 -*-

import time
from openerp import api, models


class ReportFinishedProducts(models.AbstractModel):
    _name = "report.mrp_brewing.stock_finished_products"

    def get_stock_moves(self, data):
        lines = self.env["stock.move"].search(
            [
                ("state", "=", "done"),
                ("product_id.finished_product", "=", True),
            ],
            order="date asc",
        )

        return lines

    @api.multi
    def render_html(self, data):
        docs = self.env["stock.move"].browse(self.env.context.get("active_id"))
        report_lines = self.get_stock_moves(data.get("form"))
        docargs = {
            "doc_ids": self.ids,
            "doc_model": "stock.move",
            "data": data["form"],
            "docs": docs,
            "time": time,
            "get_stock_moves": report_lines,
        }
        return self.env["report"].render(
            "mrp_brewing.stock_finished_products", docargs
        )
