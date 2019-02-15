# -*- coding: utf-8 -*-
from odoo import models, fields


class DeliveryCarrier(models.Model):
    _inherit = 'delivery.carrier'

    auto_send_picking = fields.Boolean(string="Auto send delivery mail")
    auto_send_invoice = fields.Boolean(string="Auto send invoice mail")
