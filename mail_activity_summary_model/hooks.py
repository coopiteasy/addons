from odoo import SUPERUSER_ID, api


def post_init_hook(cr, _):
    env = api.Environment(cr, SUPERUSER_ID, {})

    cr.execute(
        """
        SELECT id, summary
        FROM mail_activity
        WHERE summary IS NOT NULL"""
    )
    results = cr.fetchall()
    for id, summary in results:
        # Call inverse function
        env["mail.activity"].browse(id).summary = summary
