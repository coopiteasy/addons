# -*- coding: utf-8 -*-
from odoo import http

# class CieInfra(http.Controller):
#     @http.route('/cie_infra/cie_infra/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cie_infra/cie_infra/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('cie_infra.listing', {
#             'root': '/cie_infra/cie_infra',
#             'objects': http.request.env['cie_infra.cie_infra'].search([]),
#         })

#     @http.route('/cie_infra/cie_infra/objects/<model("cie_infra.cie_infra"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cie_infra.object', {
#             'object': obj
#         })