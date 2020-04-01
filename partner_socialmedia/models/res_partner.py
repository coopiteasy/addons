# -*- coding: utf-8 -*-
# Copyright 2018 Humanitarian Logistics Organisation e.V. - Stefan Becker
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResPartner(models.Model):
    """Add social media fields"""
    _inherit = "res.partner"

    facebook = fields.Char(translate=True)
    twitter = fields.Char(translate=True)
    skype = fields.Char(translate=True)
    linkedin = fields.Char(translate=True)
    mastodon = fields.Char(translate=True)
