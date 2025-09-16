# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later


import datetime

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


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
            order.is_gift = any(order.order_line.product_id.mapped("is_gift"))

    @api.constrains("order_line")
    def _check_gift_alone(self):
        """Ensure gift are not mixed in a sale order."""
        for order in self:
            lines_to_check = order._exclude_delivery_order_line()
            if lines_to_check:
                if not self._is_product_compatible(lines_to_check.product_id):
                    raise ValidationError(
                        _(
                            "Cannot add product gift in an order that "
                            "contains other product that are not gifts."
                        )
                    )

    @api.model
    def _is_product_compatible(self, product_ids):
        at_least_one_gift = any(product_ids.mapped("is_gift"))
        is_all_gift = all(product_ids.mapped("is_gift"))
        return is_all_gift or not at_least_one_gift

    def _exclude_delivery_order_line(self):
        """Return the order_lines that are not delivery"""
        self.ensure_one()
        return self.order_line.filtered(lambda r: not r.is_delivery)

    def check_product_compatibility(self, product_id):
        warning = super().check_product_compatibility(product_id)
        lines_to_check = self._exclude_delivery_order_line()
        product = self.env["product.product"].browse(product_id).exists()
        if not warning and lines_to_check and product:
            is_product_compatible = self._is_product_compatible(
                lines_to_check.product_id | product
            )
            if not is_product_compatible:
                if product.is_gift:
                    warning = _(
                        f"Product {product.name} cannot be added because "
                        "it's a gift and gift must be purchase seperatly."
                    )
                else:
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
                    and r not in r.contract_id.contract_line_ids.sale_order_line_id
                )
            )
            existing_partners = self.find_contact_partners(order.partner_shipping_id)
            if existing_partners:
                contract_partner = existing_partners[0]
            else:
                # We prefer that the contract owner be a 'contact'
                # partner rather than a 'delivery' partner. Granting
                # the delivery partner access to e-commerce can cause
                # issues in terms of invoicing.
                contract_partner = self.env["res.partner"].create(
                    {
                        "name": order.partner_shipping_id.name,
                        "type": "contact",
                        "parent_id": False,
                        "email": order.partner_shipping_id.email,
                        "phone": order.partner_shipping_id.phone,
                        "mobile": order.partner_shipping_id.mobile,
                        "street": order.partner_shipping_id.street,
                        "street2": order.partner_shipping_id.street2,
                        "zip": order.partner_shipping_id.zip,
                        "city": order.partner_shipping_id.city,
                        "state_id": order.partner_shipping_id.state_id.id,
                        "country_id": order.partner_shipping_id.country_id.id,
                    }
                )
            for line in line_to_create_contract:
                date_start = line.date_start
                if not date_start:
                    raise UserError(
                        _(
                            "Sales orders lines with a gift product must have a gift date."
                        )
                    )
                try:
                    date_end = datetime.date(
                        year=date_start.year + 1,
                        month=date_start.month,
                        day=date_start.day,
                    )
                except ValueError:
                    # ValueError are raised if the date does not exist.
                    # E.g. 29 february of a non leap year
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

        # If there is several results we try to eliminate some results.
        # We look for result with the same country_id.
        # If there is no match with contry_id, then we try to filter for
        # another field.
        # If there is several matches with country_id, the we try to
        # filter with another field.
        # If there is only one match with contry_id, then we return this
        # result.
        #
        # At the end, if there is several result that we cannot filter
        # more than we return all theses results
        if result:
            for field in fields_to_compare:
                filtered_partners = result.filtered(
                    lambda r: r[field] == partner[field]
                )
                nb_filtered_partners = len(filtered_partners)
                if nb_filtered_partners > 0:
                    result = filtered_partners
                if nb_filtered_partners == 1:
                    break

        return result

    @api.model
    def cron_autoconfirm_gift_order(self):
        """Auto confirm gift order"""
        orders = self.env["sale.order"].search(
            [("state", "=", "sent"), ("is_gift", "=", True)]
        )
        orders.action_confirm()
