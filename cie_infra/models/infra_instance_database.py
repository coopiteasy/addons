from odoo import models
from odoo import fields
from odoo import api
from odoo import _
import requests
import json
from werkzeug.exceptions import BadRequest, InternalServerError, NotFound
from odoo.exceptions import AccessDenied, Warning as UserError

class Database(models.Model):
    _name = 'infra.instance.database'
    _description = 'database'
    name=fields.Char('name', required=True)
    instance_id=fields.Many2one('infra.instance', string='instance')
    installed_module_ids=fields.One2many(
        comodel_name='infra.instance.module.info',
        inverse_name='database_id',
        string='installed_module')

    @api.multi
    def http_get(self, url, params, headers):
        self.ensure_one()
        if url.startswith("/"):
            url = self.url + url
        return requests.get(url,params,headers)

    def _process_response(self, response):
        if response.status_code == 200:
            content = response.content.decode("utf-8")
            return json.loads(content)
        elif response.status_code == 400:
            content = response.content.decode("utf-8")
            raise BadRequest("%s" % content)
        elif response.status_code == 403:
            raise AccessDenied(
                _("You are not allowed to access this resource")
            )
        elif response.status_code == 404:
            raise NotFound(
                _("Resource not found %s on server" % response.status_code)
            )
        else:  # 500 et al.
            content = response.content.decode("utf-8")
            raise InternalServerError(_("%s" % content))

    @api.multi
    def http_get_content(self, url, params=None, headers=None):
        self.ensure_one()
        response = self.http_get(url, params=params, headers=headers)
        return self._process_response(response)


    def cron_get_module(self):
        """
        thanks to http request, the cron will recover daily
        the different database based on a odoo's instance
        """

        databases = self.env['infra.instance.database'].search([])
        for database in databases:
            route = "/server-info/databases/"+database.name+"/modules"
            modules = database.http_get_content(route)
            for module in modules:
                if not self.is_module_already_installed(module):
                    new_module = self.env['infra.instance.module'].create({
                        "name": module["name"],
                    })
                    module_info=self.env["infra.instance.module.info"].create({
                        "installed_version": module["published_version"],
                    })
                    new_module.write({
                        "module_info_ids": module_info.id,
                    })
                    module_info.write({
                        "module_id":new_module.id,
                    })
                    database.write({
                        "installed_module_ids":  module_info.id,
                    })
        return

    def is_module_already_installed(self,module):
        modules = self.env["infra.instance.module"].search([])
        for old_module in modules:
            if module["name"] == old_module.name:
                return 1
        return 0


