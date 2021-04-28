# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging

from odoo import _
from odoo.addons.web.controllers.main import Home
from odoo.exceptions import UserError
from odoo.http import request

_logger = logging.getLogger(__name__)


class AuthSignupHome(Home):

    def do_signup(self, qcontext):
        """ Shared helper that creates a res.partner out of a token """
        values = {
            key: qcontext.get(key) for key in ('login',
                                               'name',
                                               'password',
                                               'is_company',
                                               'vat'
                                               )
        }
        if not values:
            raise UserError(_("The form was not properly filled in."))
        if values.get('password') != qcontext.get('confirm_password'):
            raise UserError(_("Passwords do not match; please retype them."))

        res_lan_obj = request.env['res.lang']

        supported_langs = [
            l['code'] for l in res_lan_obj.sudo().search_read([], ['code'])
        ]
        if request.lang in supported_langs:
            values['lang'] = request.lang
        self._signup_with_values(qcontext.get('token'), values)
        request.env.cr.commit()