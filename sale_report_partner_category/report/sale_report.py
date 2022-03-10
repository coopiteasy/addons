from odoo import fields, models


class SaleReport(models.Model):
    _inherit = "sale.report"

    category_id = fields.Many2one(
        "res.partner.category", string="Partner Category", readonly=True
    )

    def _query(self, with_clause="", fields=None, groupby="", from_clause=""):
        if fields is None:
            fields = {}
        select_str = """ ,
            pcr.category_id as category_id
        """
        fields.update(
            {
                "category_id": select_str,
            }
        )
        from_clause += (
            "left join res_partner_res_partner_category_rel pcr "
            "on (pcr.partner_id=s.partner_id)"
        )
        groupby += """,
            pcr.category_id
        """

        return super(SaleReport, self)._query(with_clause, fields, groupby, from_clause)
