# SPDX-FileCopyrightText: 2026 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import models
from odoo.tools import check_index_exist, index_exists


class AccountEdiProxyClientPeppolUser(models.Model):
    _inherit = "account_edi_proxy_client_peppol.user"

    def init(self):
        result = super().init()
        if index_exists(
            self.env.cr,
            "account_edi_proxy_client_peppol_user_unique_active_edi_identification",
        ):
            self.env.cr.execute(
                """
                DROP INDEX account_edi_proxy_client_peppol_user_unique_active_edi_identification
                """
            )
            # even if we redefine _sql_constraints in this class (without the
            # unique_active_edi_identification constraint), odoo will still
            # read them from the parent class and check that the index exists
            # after calling this. we need to remove the check to avoid having
            # it fail.
            queue = self.env.registry._post_init_queue
            for i, e in enumerate(queue):
                if (
                    e.func == check_index_exist
                    and e.args[1]
                    == "account_edi_proxy_client_peppol_user_unique_active_edi_identification"
                ):
                    del queue[i]
                    break
        return result
