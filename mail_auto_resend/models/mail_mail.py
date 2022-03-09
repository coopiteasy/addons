import logging

from odoo import api, models

_logger = logging.getLogger(__name__)


class MailMail(models.Model):
    _inherit = "mail.mail"

    @api.multi
    def _cron_resend_failed_mails(self):
        failed_mails = self.search([("state", "=", "exception")])
        try:
            failed_mails.write({"state": "outgoing"})
            self.env.cr.commit()  # pylint: disable=invalid-commit
            _logger.debug("Batch of previously failed emails are now outgoing")
        except Exception:
            self.env.cr.rollback()
            _logger.exception("An error occured while changing failed emails' state")
