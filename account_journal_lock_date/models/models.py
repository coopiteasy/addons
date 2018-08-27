# -*- coding: utf-8 -*-

from openerp import models, fields, api
from openerp.exceptions import ValidationError, UserError


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    journal_lock_date = fields.Date(
        name='Lock Date',
        help="Moves cannot be entered nor modified in this "
             "journal prior to the lock date, unless the user "
             "has the Adviser role.",
    )

    @api.model
    def _can_bypass_journal_lock_date(self):
        """ This method is meant to be overridden to provide
        finer control on who can bypass the lock date """
        return self.env.user.has_group('account.group_account_manager')


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.multi
    def _check_lock_date(self):
        res = super(AccountMove, self)._check_lock_date()

        if self.env['account.journal']._can_bypass_journal_lock_date():
            return res

        for move in self:
            lock_date = move.journal_id.journal_lock_date
            if lock_date and move.date <= lock_date:
                raise JournalLockDateError("You cannot add/modify entries "
                                               "prior to and inclusive of the "
                                               "journal lock date "
                                               " %s" % lock_date)
        return res


class JournalLockDateError(ValidationError):
    pass
