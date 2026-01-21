# SPDX-FileCopyrightText: 2026 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from psycopg2 import sql

from odoo import models


class AccountEdiProxyClientPeppolUser(models.Model):
    _inherit = "account_edi_proxy_client_peppol.user"

    def init(self):
        # this method is called after _auto_init() from the
        # account_peppol_backport module. there seems to be no clean way to
        # call code before that method. instead, we check that the index has
        # the correct definition, and if not, we modify it.
        result = super().init()
        index_name = (
            "account_edi_proxy_client_peppol_user_unique_active_edi_identification"
        )
        self.env.cr.execute(
            "select indexdef from pg_indexes where indexname = %(index_name)s",
            dict(index_name=index_name),
        )
        row = self.env.cr.fetchone()
        if row is None or "company_id" not in row[0]:
            if row is not None:
                self.env.cr.execute(
                    sql.SQL("drop index {index_name}").format(
                        index_name=sql.Identifier(index_name)
                    )
                )
            # add company_id to the index condition, as this module enables
            # multiple companies to share the same edi_identification, but
            # there should be only one record per edi_identification per
            # company.
            self.env.cr.execute(
                sql.SQL(
                    """
                    create unique index {index_name}
                    on account_edi_proxy_client_peppol_user
                        (company_id, edi_identification, proxy_type, edi_mode)
                    where (active = true)
                    """
                ).format(index_name=sql.Identifier(index_name))
            )
        return result
