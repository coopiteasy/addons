from odoo import models, fields

class Instance(models.Model):
	_name='infra.instance'
	_description='instance'
	name=fields.Char('name', required=True)
	url=fields.Html('URL')
	note=fields.Text('text')
	server_id=fields.Many2one('infra.server', string='server')
	database_ids=fields.One2many('infra.instance.database','instance_id',string='database')

