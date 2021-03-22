from odoo import api, fields, models


class ReportStockPicking(models.AbstractModel):
    _name = "report.stock.report_picking"

    @api.model
    def get_report_values(self, docids, data=None):
        """Workaround to set the record as `printed`
        when printing through 'Print > Picking Operations'.
        """
        for picking_id in docids:
            self.env["stock.picking"].browse(picking_id).set_printed(
                fields.Datetime.now()
            )

        report_obj = self.env["ir.actions.report"]
        report = report_obj._get_report_from_name("stock.report_picking")
        docargs = {
            "doc_ids": docids,
            "doc_model": report.model,
            "docs": self.env["stock.picking"].browse(docids),
        }
        return docargs
