# Copyright 2021 Coop IT Easy SCRLfs
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class Company(models.Model):
    _inherit = "res.company"

    fallback_account_id = fields.Many2one(
        comodel_name="account.account",
        string="Fallback Account",
        help="Moves for which the tax was undefined will be assigned to this account.",
        # This field is technically required, but can't be set to required,
        # because res.company row(s) already exist before the installation of
        # this module.
        # required=True,
    )
