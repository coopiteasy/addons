# -*- coding: utf-8 -*-

# Copyright 2018 Rémy Taymans <remytaymans@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


from openerp import models, fields


class Partner(models.Model):
    _inherit = 'res.partner'

    communication_lang_id = fields.Many2one('res.partner.communication.lang',
                                            string="Communication Language")


class PartnerCommunicationLang(models.Model):
    _name = 'res.partner.communication.lang'
    _description = "Partner Communication Lang"
    _order = 'name'

    name = fields.Char("Name", required=True)
    partner_ids = fields.One2many('res.partner', 'communication_lang_id',
                                  string="Partners")
    active = fields.Boolean("Active", default=True)
