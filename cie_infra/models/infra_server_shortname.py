from odoo import fields, models

class Server_shortname(models.Model):
	_name='infra.server.shortname'
	_description='server.shortname'
	name=fields.Char('name')
	server_id=fields.Many2one('infra.server',string='server')

