from odoo import fields, models


class Database(models.Model):
	_name='infra.instance.database'
	_description='database'
	name=fields.Char('name', required=True)
	instance_id=fields.Many2one('infra.instance',string='instance')
	installed_module_ids=fields.One2many('infra.instance.module.info','database_id',string='installed_module')



