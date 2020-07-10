# -*- coding: utf-8 -*-
# (c) 2015 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp.addons.decimal_precision import decimal_precision as dp

from openerp import models, fields, api
from openerp.tools import config


class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    _track = {
        'state': {
            'mrp_bom_version.mt_active': lambda self, cr, uid, obj,
            ctx=None: obj.state == 'active',
        },
    }

    @api.one
    def _get_old_versions(self):
        parent = self.parent_bom
        old_version = self.env['mrp.bom']
        while parent:
            old_version += parent
            parent = parent.parent_bom
        self.old_versions = old_version

    def _default_active(self):
        """Needed for preserving normal flow when testing other modules."""
        res = False
        if config['test_enable']:
            res = not bool(self.env.context.get('test_mrp_bom_version'))
        return res

    def _default_state(self):
        """Needed for preserving normal flow when testing other modules."""
        res = 'draft'
        if (config['test_enable'] and
                not self.env.context.get('test_mrp_bom_version')):
            res = 'active'
        return res

    active = fields.Boolean(
        default=_default_active,
        readonly=True, states={'draft': [('readonly', False)]})
    historical_date = fields.Date(string='Historical Date', readonly=True)
    state = fields.Selection([('draft', 'Draft'), ('active', 'Active'),
                   ('historical', 'Historical')], string='State',
                    index=True, readonly=True, default=_default_state, copy=False)
    product_tmpl_id = fields.Many2one('product.template', string='Product', domain="[('type', 'in', ['product', 'consu'])]", required=True,
        readonly=True, states={'draft': [('readonly', False)]})
    product_id = fields.Many2one('product.product', string='Product Variant',
            domain="['&', ('product_tmpl_id','=',product_tmpl_id), ('type', 'in', ['product', 'consu'])]",
            readonly=True, states={'draft': [('readonly', False)]},
            help="If a product variant is defined the BOM is available only for this product.")
    product_qty = fields.Float(string='Product Quantity', required=True, digits_compute=dp.get_precision('Product Unit of Measure'),
        readonly=True, states={'draft': [('readonly', False)]})
#     name = fields.Char(
#         states={'historical': [('readonly', True)]})
    code = fields.Char(string='Reference',
        states={'historical': [('readonly', True)]})
    type = fields.Selection([('normal','Manufacture this product'),('phantom','Ship this product as a set of components (kit)')], 'BoM Type', required=True,
        states={'historical': [('readonly', True)]},
        help= "Set: When processing a sales order for this product, the delivery order will contain the raw materials, instead of the finished product.")
    company_id = fields.Many2one('res.company', string='Company', required=True,
        states={'historical': [('readonly', True)]})
    product_uom = fields.Many2one('product.uom',
        states={'historical': [('readonly', True)]},
        string='Product Unit of Measure', required=True, help="Unit of Measure (Unit of Measure) is the unit of measurement for the inventory control")
    routing_id = fields.Many2one('mrp.routing', 'Routing', 
        readonly=True, states={'draft': [('readonly', False)]},
        help="The list of operations (list of work centers) to produce the finished product. "\
        "The routing is mainly used to compute work center costs during operations and to plan future loads on work centers based on production planning.")
    bom_line_ids = fields.One2many('mrp.bom.line', 'bom_id', string='BoM Lines', copy=True,
        readonly=True, states={'draft': [('readonly', False)]})
    position = fields.Char(string='Internal Reference', 
        states={'historical': [('readonly', True)]},help="Reference to a position in an external plan.")
    date_start = fields.Date(string='Valid From', help="Validity of this BoM. Keep empty if it's always valid.",
        states={'historical': [('readonly', True)]})
    date_stop = fields.Date(string='Valid Until', help="Validity of this BoM. Keep empty if it's always valid.",
        states={'historical': [('readonly', True)]})
    property_ids = fields.Many2many('mrp.property', string='Properties',
        states={'historical': [('readonly', True)]})
    product_rounding = fields.Float(string='Product Rounding', help="Rounding applied on the product quantity.",
        states={'historical': [('readonly', True)]})
    product_efficiency = fields.Float(string='Manufacturing Efficiency', required=True,
        states={'historical': [('readonly', True)]}, help="A factor of 0.9 means a loss of 10% during the production process.",)
#     message_follower_ids = fields.Many2many(
#         states={'historical': [('readonly', True)]})
#     message_ids = fields.One2many(
#         states={'historical': [('readonly', True)]})
    version = fields.Integer(states={'historical': [('readonly', True)]},
                             copy=False, default=1)
    parent_bom = fields.Many2one(comodel_name='mrp.bom', string='Parent BoM')
    old_versions = fields.Many2many(
        comodel_name='mrp.bom', string='Old Versions',
        compute='_get_old_versions')
    default = fields.Boolean(string="Default BOM")

    @api.multi
    def button_draft(self):
        active_draft = self.env['mrp.config.settings']._get_parameter(
            'active.draft')
        self.write({
            'active': active_draft and active_draft.value or False,
            'state': 'draft',
        })

    @api.multi
    def button_new_version(self):
        self.ensure_one()
        new_bom = self._copy_bom()
        self.button_historical()
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form, tree',
            'view_mode': 'form',
            'res_model': 'mrp.bom',
            'res_id': new_bom.id,
            'target': 'current',
        }

    def _copy_bom(self):
        active_draft = self.env['mrp.config.settings']._get_parameter(
            'active.draft')
        new_bom = self.copy({
            'version': self.version + 1,
            'active': active_draft and active_draft.value or False,
            'parent_bom': self.id,
        })
        if self.type == 'normal':
            for bom_line in self.bom_line_ids:
                if (bom_line.product_id.product_tmpl_id.bom_ids
                        and bom_line.product_id.product_tmpl_id.bom_count > 0):
                    for bom in bom_line.product_id.product_tmpl_id.bom_ids:
                        if bom.version == self.version:
                            bom.button_new_version()
        return new_bom

    @api.multi
    def button_activate(self):
        self.write({
            'active': True,
            'state': 'active'
        })

    @api.multi
    def button_historical(self):
        self.write({
            'active': False,
            'state': 'historical',
            'historical_date': fields.Date.today()
        })

    def search(self, cr, uid, args, offset=0, limit=None, order=None,
               context=None, count=False):
        """Add search argument for field type if the context says so. This
        should be in old API because context argument is not the last one.
        """
        if context is None:
            context = {}
        search_state = context.get('state', False)
        if search_state:
            args += [('state', '=', search_state)]
        return super(MrpBom, self).search(
            cr, uid, args, offset=offset, limit=limit, order=order,
            context=context, count=count)

    @api.model
    def _bom_find(
            self, product_tmpl_id=None, product_id=None, properties=None):
        """ Finds BoM for particular product and product uom.
        @param product_tmpl_id: Selected product.
        @param product_uom: Unit of measure of a product.
        @param properties: List of related properties.
        @return: False or BoM id.
        """
        bom_id = super(MrpBom, self.with_context(state='active'))._bom_find(
            product_tmpl_id=product_tmpl_id, product_id=product_id,
            properties=properties)
        return bom_id

    @api.multi
    def name_get(self):
        res = []
        for record in self:
            name = record.product_tmpl_id.name
            if record.version:
                name = '[version %s] %s' % (record.version, name)
            res.append((record.id, name))
        return res
