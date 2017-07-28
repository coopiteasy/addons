# -*- coding: utf-8 -*-

from openerp import api, fields, models, _

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    quantity_to_deliver = fields.Float(string="Default quantity to deliver")
    deposit_point = fields.Boolean(string="Deposit/Sale")
    carrier_delivery = fields.Boolean(string="Carrier delivery")
    carrier_id = fields.Many2one('res.partner', string="Assigned carrier", domain=[('carrier_delivery','=',True)])
    
    