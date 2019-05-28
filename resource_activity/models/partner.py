# -*- coding: utf-8 -*-
# Copyright 2018 Coop IT Easy SCRLfs.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    def _resource_activity_count(self):
        for partner in self:
            partner.activity_count = len(partner.resource_activities)

    is_guide = fields.Boolean(string="Guide")
    is_trainer = fields.Boolean(string="Trainer")
    is_partner = fields.Boolean(string="Partner")
    resource_activities = fields.One2many('resource.activity','partner_id', string="Activities")
    activity_count = fields.Integer(string='# of Activities', compute=_resource_activity_count)
    resource_location_guide = fields.Many2one('resource.location', string="Guide Location")
    resource_location_trainer = fields.Many2one('resource.location', string="Trainer location")
