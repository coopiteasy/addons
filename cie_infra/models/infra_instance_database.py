from odoo import fields, models


class Database(models.Model):
    _name = 'infra.instance.database'
    _description = 'database'
    name=fields.Char('name', required=True)
    instance_id=fields.Many2one('infra.instance', string='instance')
    installed_module_ids=fields.One2many(
        comodel_name='infra.instance.module.info',
        inverse_name='database_id',
        string='installed_module')


    def cron_get_database(self):
        """
        thanks to http request, the cron will recover daily
        the different database based on a odoo's instance
        """
        route="/web/database/list_database"
        databases = self.env['infra.instance'].http_get_content(route)
        instance = self.env['infra.instance'].search([])
        for db in databases["databases"]:
            self.env["infra.instance.database"].create({
                "name": db,
                "instance_id":instance
            })
        db_instance=


