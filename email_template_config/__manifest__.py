# Copyright 2018-Coop IT Easy SCRLfs (<http://www.coopiteasy.be>)
# - Houssine BAKKALI - <houssine@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Email Configuration",
    "version": "12.0.1.0.0",
    "depends": ["mail"],
    "author": "Coop IT Easy SCRLfs",
    "category": "Discuss",
    "website": "https://coopiteasy.be",
    "license": "AGPL-3",
    "summary": """
    This module extends the email in order to force some behaviours
    configured in the mail template(e.g. force send mail or not).
    """,
    "data": ["views/mail_template_views.xml"],
    "installable": True,
}
