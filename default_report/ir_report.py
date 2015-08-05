import openerp
from openerp.osv import fields, orm

class ir_actions_report_xml(orm.Model):
    _inherit = 'ir.actions.report.xml'
    _columns = {
        'is_default': fields.boolean('Is default',
            help="This field marks the report as default report for this model.")
    }
    
    def write(self, cr, uid, ids, vals, context=None):
        if 'is_default' in vals.keys() and vals.get('is_default') == True:
            reports_ids = self.search(cr,uid, [('is_default','=',True)])
            if reports_ids : 
                super(ir_actions_report_xml, self).write(cr, uid, reports_ids, {'is_default':False}, context)
        return super(ir_actions_report_xml, self).write(cr, uid, ids, vals, context=context)