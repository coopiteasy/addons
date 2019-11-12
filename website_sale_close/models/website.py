# -*- coding: utf-8 -*-
# Copyright 2019 Coop IT Easy SCRLfs
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class Website(models.Model):

    _inherit = "website"

    is_ecommerce_open = fields.Boolean(
        string="Is e-commerce open",
        default=False,
        help="When checked, e-commerce is open. When unchecked, "
        "e-commerce is closed.",
    )
    text_closed_ecommerce = fields.Html(
        string="Text closed e-commerce",
        default="E-commerce is momently closed.", translate=True
    )
