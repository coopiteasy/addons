# -*- coding: utf-8 -*-

# Copyright 2018 Rémy Taymans <remytaymans@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


from openerp import models, fields


class Partner(models.Model):
    _inherit = 'res.partner'

    communication_tag_ids = fields.Many2many('res.partner.communication.tag',
                                             string="Communication")


class PartnerCommunicationTag(models.Model):
    _name = 'res.partner.communication.tag'
    _description = "Partner Communication Tag"
    _order = 'name'

    name = fields.Char("Name", required=True)
    description = fields.Text("Description")
    partner_ids = fields.Many2many('res.partner', string="Partners")
    active = fields.Boolean("Active", default=True)
