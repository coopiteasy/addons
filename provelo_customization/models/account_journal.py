# Copyright 2020 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import models, _, api
from openerp.exceptions import ValidationError


class AccountJournal(models.Model):
    _inherit = "account.journal"

    @api.multi
    @api.constrains("code")
    def _check_code_length(self):
        for journal in self:
            if journal.active and journal.code and len(journal.code) > 4:
                raise ValidationError(_(
                    "Journal code cannot be longer than 4 characters"
                ))
