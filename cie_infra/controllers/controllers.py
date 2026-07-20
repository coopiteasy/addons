from odoo import http

class CieInfra(http.Controller):
     #@http.route('/cie_infra/index', auth='public')
     #def index(self, **kw):
      #   return "Hello, world"

     @http.route('/cie_infra/server/', auth='public')
     def list_server(self, **kw):
         server=http.request.env['infra.server']
         servers=server.search([])
         return http.request.render('cie_infra.server_list_template', {
             'servers': servers
         })
#     @http.route('/cie_infra/cie_infra/objects/<model("cie_infra.cie_infra"):obj>/', auth='public')
#     def object(self, obj, **kw):
#          return http.request.render('cie_infra.object', {
#             'object': obj
#        })
