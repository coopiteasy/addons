# © 2016 Houssine BAKKALI, Open Architects Consulting SPRL
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from datetime import datetime

from dateutil.relativedelta import relativedelta

from odoo import SUPERUSER_ID, api, fields, models

from odoo.addons import decimal_precision as dp

UNIT = dp.get_precision("Product Unit of Measure")


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    autoload_all_products = fields.Boolean(
        string="Auto-load all products", default=False
    )

    @api.onchange("partner_id", "company_id")
    def onchange_partner_id(self):
        super(PurchaseOrder, self).onchange_partner_id()
        self.order_line = self.create_order_line()
        return {}

    @api.model
    def create_order_line(self):
        res = []
        if self.autoload_all_products:
            fpos = self.fiscal_position_id
            for supplier_info in self.env["product.supplierinfo"].search(
                [
                    ("name", "=", self.partner_id.id),
                    ("product_tmpl_id.active", "=", True),
                    ("product_tmpl_id.purchase_ok", "=", True),
                ]
            ):
                values = {}
                values["order_id"] = self.id
                values[
                    "product_id"
                ] = supplier_info.product_tmpl_id.product_variant_ids[0].id
                values["product_qty"] = supplier_info.min_qty
                values["product_uom"] = supplier_info.product_uom.id
                values["price_unit"] = supplier_info.price
                product_lang = supplier_info.product_tmpl_id.product_variant_ids[
                    0
                ].with_context(
                    {
                        "lang": self.partner_id.lang,
                        "partner_id": self.partner_id.id,
                    }
                )
                name = product_lang.display_name
                if product_lang.description_purchase:
                    name += "\n" + product_lang.description_purchase
                values["name"] = name
                if self.date_order:
                    values["date_planned"] = self.date_order + relativedelta(
                        days=supplier_info.delay if supplier_info else 0
                    )
                else:
                    values["date_planned"] = datetime.today() + relativedelta(
                        days=supplier_info.delay if supplier_info else 0
                    )
                if self.env.uid == SUPERUSER_ID:
                    company_id = self.env.user.company_id.id
                    values["taxes_id"] = fpos.map_tax(
                        supplier_info.product_tmpl_id.supplier_taxes_id.filtered(
                            lambda r: r.company_id.id == company_id
                        )
                    )
                else:
                    values["taxes_id"] = fpos.map_tax(
                        supplier_info.product_tmpl_id.supplier_taxes_id
                    )

                res.append(values)
        return res
