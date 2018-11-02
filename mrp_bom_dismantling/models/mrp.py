# -*- coding: utf-8 -*-
# © 2016 Robin Keunen, Coop IT Easy SCRL fs
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models, _
from itertools import chain


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    master_mo_candidate_ids = fields.Many2many(
        'mrp.production',
        string='Master MO Candidates',
        compute='_compute_master_mo_candidate',
    )

    @api.model
    def create(self, vals):
        result = super(MrpProduction, self).create(vals)

        if result.bom_id.dismantling and len(result.master_mo_candidate_ids) > 0:  # noqa
            result.master_mo_id = (
                result
                .master_mo_candidate_ids
                .sorted(key=lambda mo: mo.date_planned)[0]
            )
        return result

    # todo move this to create since never used elsewhere
    @api.multi
    @api.depends('bom_id')
    def _compute_master_mo_candidate(self):
        for production in self:
            source_products = (
                production
                .bom_id
                .bom_line_ids
                .mapped('product_id')
            )

            master_mos = (p.compute_master_mo_candidates() for p in source_products)
            master_mo_ids = list(chain.from_iterable(mos.ids for mos in master_mos))

            production.master_mo_candidate_ids = [(6, False, master_mo_ids)]
