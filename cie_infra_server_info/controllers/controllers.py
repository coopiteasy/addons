# -*- coding: utf-8 -*-
import odoo
from odoo import http
from contextlib import closing

class CieInfraDatasend(http.Controller):
#     @http.route('/cie_infra_server_info/cie_infra_server_info/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cie_infra_server_info/cie_infra_server_info/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('cie_infra_server_info.listing', {
#             'root': '/cie_infra_server_info/cie_infra_server_info',
#             'objects': http.request.env['cie_infra_server_info.cie_infra_server_info'].search([]),
#         })

#     @http.route('/cie_infra_server_info/cie_infra_server_info/objects/<model("cie_infra_server_info.cie_infra_server_info"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cie_infra_server_info.object', {
#             'object': obj
#         })

    @http.route("/web/database/list_database", type="http", auth="none")
    def databaselist(self, **kw):
        result = ""
        list_db = http.db_list()
        result += " ".join(list_db)
        return result

    @http.route("/web/database/<string:dbname>/modules", type="http", auth="none")
    def modulelist(self,dbname, **kw):
        list_db = http.db_list()
        # List installed modules
        modules = []
        db = odoo.sql_db.db_connect(dbname)
        with closing(db.cursor()) as cr:
            cr.execute("SELECT name, latest_version, published_version, state, shortdesc FROM ir_module_module WHERE state = 'installed'")
            modules.append(cr.fetchall())
        return str(modules)
