# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later


import datetime

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    is_gift = fields.Boolean(compute="_compute_is_gift")
    gift_date = fields.Date(compute="_compute_gift_date")

    @api.depends("order_line")
    def _compute_gift_date(self):
        """Get gift_date from date_start on order_line"""
        for order in self:
            dates = order.order_line.filtered(lambda r: r.product_id.is_gift).mapped(
                "date_start"
            )
            order.gift_date = dates[0] if dates else False

    @api.depends("order_line")
    def _compute_is_gift(self):
        """Tell if an order is a gift or not"""
        for order in self:
            order.is_gift = any(order.order_line.mapped("product_id").mapped("is_gift"))

    @api.constrains("order_line")
    def _check_gift_alone(self):
        """Ensure gift are not mixed in a sale order."""
        for order in self:
            if self.order_line:
                at_least_one_gift = any(
                    order.order_line.mapped("product_id").mapped("is_gift")
                )
                is_all_gift = all(
                    order.order_line.mapped("product_id").mapped("is_gift")
                )
                if at_least_one_gift and not is_all_gift:
                    raise ValidationError(
                        _(
                            "Cannot add product gift in an order that "
                            "contains other product that are not gifts."
                        )
                    )

    def check_product_compatibility(self, product_id):
        warning = super().check_product_compatibility(product_id)
        if not warning and self.order_line:
            product = self.env["product.product"].browse(product_id).exists()
            non_gifts = self.order_line.mapped("product_id").filtered(
                lambda p: not p.is_gift
            )
            is_all_gift = all(self.order_line.mapped("product_id").mapped("is_gift"))
            if product:
                if product.is_gift and non_gifts:
                    warning = _(
                        f"Product {product.name} cannot be added because "
                        "it's a gift and gift must be purchase seperatly."
                    )
                elif not product.is_gift and is_all_gift:
                    warning = _(
                        f"Product {product.name} cannot be added because "
                        "it is not a gift and other product are gifts."
                    )
        return warning

    def action_confirm(self):
        """Create contract for gift product"""
        contract_model = self.env["contract.contract"]
        for order in self.filtered("is_gift"):
            line_to_create_contract = order.order_line.filtered(
                lambda r: not r.contract_id and r.product_id.is_gift
            )
            line_to_update_contract = order.order_line.filtered(
                lambda r: (
                    r.contract_id
                    and r.product_id.is_gift
                    and r
                    not in r.contract_id.contract_line_ids.mapped("sale_order_line_id")
                )
            )
            existing_partners = self.find_contact_partners(order.partner_shipping_id)
            if existing_partners:
                contract_partner = existing_partners[0]
            else:
                contract_partner = order.partner_shipping_id.copy(
                    {
                        # copy name to prevent odoo adding '(copy)'
                        # after the name.
                        "name": order.partner_shipping_id.name,
                        "type": "contact",
                        "parent_id": False,
                    }
                )
            for line in line_to_create_contract:
                date_start = line.date_start
                try:
                    date_end = datetime.date(
                        year=date_start.year + 1,
                        month=date_start.month,
                        day=date_start.day,
                    )
                except ValueError:
                    date_end = datetime.date(
                        year=date_start.year + 1,
                        month=date_start.month,
                        day=date_start.day - 1,
                    )
                contract = contract_model.create(
                    {
                        "name": f"{line.product_id.name}: {order.name}",
                        "partner_id": contract_partner.id,
                        "contract_type": "sale",
                        "is_gift": True,
                        "date_start": order.gift_date,
                        "payment_mode_id": order.payment_mode_id.id,
                        "line_recurrence": True,
                        "recurring_rule_type": "yearly",
                        "recurring_interval": 1,
                        "contract_line_ids": [
                            fields.Command.create(
                                {
                                    "sale_order_line_id": line.id,
                                    "product_id": line.product_id.id,
                                    "name": line.product_id.name,
                                    "quantity": line.product_uom_qty,
                                    "uom_id": line.product_uom.id,
                                    "price_unit": 0,
                                    "date_start": date_start,
                                    "date_end": date_end,
                                    "recurring_rule_type": "yearly",
                                    "recurring_interval": 1,
                                    "auto_renew_rule_type": "yearly",
                                    "auto_renew_interval": "1",
                                    "recurring_next_date": line.date_start,
                                }
                            ),
                        ],
                    }
                )
                contract._onchange_contract_type()
                # Cannot use "contract_id" field on order_line because
                # for a gift the partner on sale.order is not the same
                # as the partner on the contract.
                line.write({"gift_contract_id": contract.id})
            for line in line_to_update_contract:
                line.create_contract_line(line.contract_id)
        return super().action_confirm()

    @api.model
    def find_contact_partners(self, partner):
        """Find partners that are the same as :partner:"""
        partners_found = self.env["res.partner"].search(
            [
                ("email", "=", partner.email),
                ("type", "=", "contact"),
            ]
        )
        result = partners_found
        fields_to_compare = [
            "country_id",
            "zip",
            "name",
            "user_id",
        ]

        if result:
            for field in fields_to_compare:
                filtered_partners = result.filtered(lambda r: r.mapped(field))
                nb_filtered_partners = len(filtered_partners)
                if nb_filtered_partners > 0:
                    result = filtered_partners
                if nb_filtered_partners == 1:
                    break

        return result
