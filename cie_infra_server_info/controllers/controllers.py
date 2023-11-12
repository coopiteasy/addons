# -*- coding: utf-8 -*-
import odoo
from odoo import http
from contextlib import closing

class CieInfraDatasend(http.Controller):


#    @http.route("/web/database/list_database", type="http", auth="none")
#    def databaselist(self, **kw):
#        result = ""
#        list_db = http.db_list()
#        result += " ".join(list_db)
#        return result

    @http.route("/server-info/databases", type="json", auth="none")
    def databaselist(self, **kw):
        list_db = http.db_list()
        result = {"databases": list_db}
        return result

#    @http.route("/web/database/<string:dbname>/modules", type="http", auth="none")
#    def modulelist(self,dbname, **kw):
#        list_db = http.db_list()
#        # List installed modules
#        modules = []
#        db = odoo.sql_db.db_connect(dbname)
#        with closing(db.cursor()) as cr:
#            cr.execute("SELECT name, latest_version, published_version, state, shortdesc FROM ir_module_module WHERE state = 'installed'")
#            modules.append(cr.fetchall())
#        return str(modules)

    @http.route("/server-info/databases/<string:dbname>/modules", type="json", auth="none")
    def modulelist(self,dbname, **kw):
        list_db = http.db_list()
        # List installed modules
        modules = {"database":dbname}
        db = odoo.sql_db.db_connect(dbname)
        with closing(db.cursor()) as cr:
            cr.execute("SELECT name FROM ir_module_module WHERE state = 'installed'")
            modules["name"]= cr.fetchall()
            cr.execute( "SELECT latest_version FROM ir_module_module WHERE state = 'installed'")
            modules["latest_version"] = cr.fetchall()
            cr.execute("SELECT published_version FROM ir_module_module WHERE state = 'installed'")
            modules["published_version"] = cr.fetchall()
            cr.execute("SELECT state FROM ir_module_module WHERE state = 'installed'")
            modules["state"] = cr.fetchall()
            cr.execute("SELECT shortdesc FROM ir_module_module WHERE state = 'installed'")
            modules["shortdesc"] = cr.fetchall()
            #cr.execute("SELECT name,latest_version, published_version, state, shortdesc FROM ir_module_module WHERE state = 'installed'")
            #records=cr.fetchall()
            #for row in records :
                #modules["name"]=row[0]
                #modules["latest_version"]=row[1]
                #modules["published_version"]=row[2]
                #modules["state"]=row[3]
                #modules["shortdesc"]=row[4]

        return modules
