from odoo import fields, models

class Server(models.Model):
    _name = 'infra.server'
    _description = 'server'
    name = fields.Char('name', required=True)
    ipv4 = fields.Char('ipv4', required=True)
    ipv6 = fields.Char('ipv6', required=True)
    datacenter_info = fields.Char('Datacenter info')
    ovh_address = fields.Char('OVH\'s adress', required=True)
    cie_address = fields.Char('cie adress', required=True)
    note = fields.Text('text')
    datacenter_id = fields.Many2one('infra.datacenter', string='Datacenter')
    shortname_ids=fields.One2many('infra.server.shortname','server_id',string='shortname')
    instance_ids=fields.One2many('infra.instance','server_id',string='instance') 
