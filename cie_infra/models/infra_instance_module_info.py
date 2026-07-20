from odoo import fields , models

class ModuleInfo(models.Model):
	_name='infra.instance.module.info'
	_description='module.info'
	installed_version=fields.Char('installed_version',required=True)
	available_version=fields.Char('available_version')
	database_id=fields.Many2one('infra.instance.database',string='database')
	module_id=fields.Many2one('infra.instance.module',string='module')


