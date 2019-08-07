# -*- coding: utf-8 -*-

from openerp import api, fields, models, _
from openerp.exceptions import ValidationError, UserError


class ActivityDraftToDoneWizard(models.TransientModel):
    _name = "resource.activity.draft.done.wizard"

    @api.multi
    def draft_to_done(self):
        activity = (
            self.env['resource.activity']
                .browse(self._context.get('active_ids'))[0]
        )
        activity.state = 'done'
        return {'type': 'ir.actions.act_window_close'}
