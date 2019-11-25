# -*- coding: utf-8 -*-

import time
from openerp import api, models


class ReportBrewRegister(models.AbstractModel):
    _name = "report.mrp_brewing.brew_register"

    def get_brew_orders(self, data):
        lines = self.env["brew.order"].search([("state", "=", "done")])

        return lines

    @api.multi
    def render_html(self, data):
        docs = self.env["brew.order"].browse(self.env.context.get("active_id"))
        report_lines = self.get_brew_orders(data.get("form"))
        docargs = {
            "doc_ids": self.ids,
            "doc_model": "brew.order",
            "data": data["form"],
            "docs": docs,
            "time": time,
            "get_brew_orders": report_lines,
        }
        return self.env["report"].render("mrp_brewing.brew_register", docargs)
