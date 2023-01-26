# SPDX-FileCopyrightText: 2023 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    resource_booking_ids = fields.One2many(
        comodel_name="resource.booking",
        inverse_name="sale_order_line_id",
        string="Resource Booking",
    )
