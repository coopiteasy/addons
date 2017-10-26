# -*- coding: utf-8 -*-

from openerp import api, fields, models

MODEL_MAP = {
        'mrp_brewing.stock_raw_materials':'stock.move',
        'mrp_brewing.stock_finished_products':'stock.move',
        'mrp_brewing.brew_register':'brew.order'
    }

class StockReport(models.TransientModel):
    _name = "stock.report"
    _description = "Stock Report"
    
    report_name = fields.Selection([('mrp_brewing.stock_raw_materials','Raw Material Report'),
                                    ('mrp_brewing.stock_finished_products','Finished Product Report'),
                                    ('mrp_brewing.brew_register',' Brew Register Report')]
                                   ,string="report Name",required=True)
    date_from = fields.Date(string='Start Date')
    date_to = fields.Date(string='End Date')
#     target_move = fields.Selection([('posted', 'All Posted Entries'),
#                                     ('all', 'All Entries'),
#                                     ], string='Target Moves', required=True, default='posted')


#     account_report_id = fields.Many2one('account.financial.report', string='Account Reports', required=True, default=_get_account_report)
    
    def _build_contexts(self, data):
        result = {}
        #result['state'] = 'target_move' in data['form'] and data['form']['target_move'] or ''
        result['date_from'] = data['form']['date_from'] or False
        result['date_to'] = data['form']['date_to'] or False
        result['strict_range'] = True if result['date_from'] else False
        return result
    
    @api.multi
    def check_report(self):
        self.ensure_one()
        data = {}
        data['ids'] = self.env.context.get('active_ids', [])
        data['model'] = MODEL_MAP[self.report_name]
        data['form'] = self.read(['date_from', 'date_to'])[0]
        used_context = self._build_contexts(data)
        data['form']['used_context'] = dict(used_context, lang=self.env.context.get('lang', 'en_US'))
        return self.env['report'].get_action(self, self.report_name, data=data)
    
