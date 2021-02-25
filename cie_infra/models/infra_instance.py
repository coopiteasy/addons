from odoo import models
from odoo import fields
from odoo import api
from odoo import _
import requests
import json
from werkzeug.exceptions import BadRequest, InternalServerError, NotFound
from odoo.exceptions import AccessDenied, Warning as UserError


class Instance(models.Model):
    _name='infra.instance'
    _description='instance'
    name=fields.Char('name', required=True)
    url=fields.Html('URL')
    note=fields.Text('text')
    server_id=fields.Many2one('infra.server', string='server')
    database_ids=fields.One2many('infra.instance.database','instance_id', string="database")

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








