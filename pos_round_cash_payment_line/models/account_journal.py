# -*- coding: utf-8 -*-
# © 2016 Robin Keunen, Coop IT Easy SCRL fs
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    cash_rounding = fields.Boolean(
        string='Cash Rounding Journal',
        default=False,
    )
