

from openerp import models, fields, api

class AddCallsWizard(models.TransientModel):
    _name = 'add.calls.wizard'
    
    message = fields.Char(string="Message", required=True)
    
    @api.multi
    def add_message(self):
        respondent_ids = self._context.get('active_ids')
        message = self.message
        for respondent_id in respondent_ids:
           self.env['crm.phonecall'].create({'partner_id':respondent_id, 'name':message})
        return {}
