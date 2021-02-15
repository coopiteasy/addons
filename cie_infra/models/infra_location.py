from odoo import fields, models

class Location(models.Model):
	_name='infra.location'
	_description='location'
	name=fields.Char('name', required=True)
	country_id=fields.Many2one('res.country', string='country')
