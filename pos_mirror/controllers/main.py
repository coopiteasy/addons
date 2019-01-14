# -*- coding: utf-8 -*-
import werkzeug
import json
import ast

from openerp.addons.web import http
from openerp.addons.web.http import request

class PosMirror(http.Controller):
    @http.route(['/pos/mirror'], type='http', auth="public", website=True)
    def mirror(self, pos_session=None, **post):
        session = None
        if pos_session:
            session = request.env['pos.session'].sudo().search([('name', '=', pos_session)], limit=1)
            config = session.config_id
        else:
            config = request.env['pos.config'].sudo().search([], limit=1)
        request.session['session_name'] = pos_session
        return request.render('pos_mirror.pos_mirror_image', {'config': config})

    @http.route(['/pos/mirror_data'], type='http', auth="public", website=True)
    def mirror_data(self, **post):
        values = {}
        if request.session.get('session_name'):
            mirror_order = request.env['mirror.image.order'].sudo().search([('session_name', '=', str(request.session.get('session_name')))], limit=1)
            values = {'name': ast.literal_eval(mirror_order.order_line), 'currency': mirror_order.currency}
        return json.dumps(values)
