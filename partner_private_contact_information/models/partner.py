# -*- coding: utf-8 -*-

# Copyright 2018 Robin Keunen <robin@keunen.net>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


from openerp import models, fields


class Partner(models.Model):
    _inherit = 'res.partner'

    is_vip = fields.Boolean(string='VIP', default=False)

    vip_street = fields.Char('Private Street')
    vip_street2 = fields.Char('Private Street2')
    vip_zip = fields.Char('Private Zip', size=24, change_default=True)
    vip_city = fields.Char('Private City')
    vip_state_id = fields.Many2one("res.country.state", 'State', ondelete='restrict')
    vip_country_id = fields.Many2one('res.country', 'Country', ondelete='restrict')
    vip_email = fields.Char('Private Email')
    vip_phone = fields.Char('Private Phone')
    vip_mobile = fields.Char('Private Mobile')
