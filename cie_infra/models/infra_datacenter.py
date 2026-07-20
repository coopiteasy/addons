from odoo import models, fields


class Datacenter(models.Model):
    _name = 'infra.datacenter'
    _description = 'datacenter'
    name = fields.Char('Datacenter', required=True)
    location_id = fields.Many2one('infra.location', string='location')
    server_ids = fields.One2many('infra.server', 'datacenter_id', string='Server')
