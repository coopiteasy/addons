from odoo import fields, models

class Module(models.Model):
	_name='infra.instance.module'
	_description='module'
	name=fields.Char('name',required=True)
	module_info_ids=fields.One2many('infra.instance.module.info','module_id',string='module_info')

