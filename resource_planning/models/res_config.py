# -*- coding: utf-8 -*-

from openerp import SUPERUSER_ID
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT as DF
from openerp import api, fields, models, _
from openerp.exceptions import UserError
    
class ResourceConfigSettings(models.TransientModel):
    _name = 'resource.config.settings'
    _inherit = 'res.config.settings'
        
    group_multi_location = fields.Boolean(string='Allow multi location',
        implied_group='resource_planning.group_multi_location',
        help="Allows you multi location environment")
    
    @api.multi
    def set_group_multi_location(self):
        ir_model = self.env['ir.model.data']
        group_resource_user = ir_model.get_object('resource_planning', 'group_resource_user')
        group_location = ir_model.get_object('resource_planning', 'group_multi_location')
        if self.group_multi_location:
            group_resource_user.write({'implied_ids': [(4, group_location.id)]})
        return True