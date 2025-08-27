# SPDX-FileCopyrightText: 2025 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import models

from odoo.addons.sale.models.sale_order_line import SaleOrderLine as SaleSaleOrderLine


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _compute_qty_to_invoice(self):
        res = super()._compute_qty_to_invoice()
        # The product_contract module overrides the _compute_qty_to_invoice()
        # method and sets qty_to_invoice to 0 if the associated product is
        # "is_contract". This is needed because the SO that will create the
        # contract should not be invoiced. However, the
        # contract_sale_generation module allows to produce new SOs, with the
        # same products, from the contract. These SOs need to be invoiced.
        # Therefore for these SOs "created from contract", the qty_to_invoice
        # should not be set to 0, but be computed by the standard odoo method.
        for line in self:
            if line.order_id.created_from_contract:
                SaleSaleOrderLine._compute_qty_to_invoice(line)
        return res
