from odoo import api, fields, models


class MailTemplate(models.Model):
    _inherit = "mail.template"

    force_email_send = fields.Boolean(string="Force mail send?")

    @api.multi
    def send_mail(self, res_id, force_send=False, raise_exception=False):
        return super(MailTemplate, self).send_mail(
                                            res_id,
                                            force_send=self.force_email_send,
                                            raise_exception=False)
