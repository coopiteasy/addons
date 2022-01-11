# Copyright 2019 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


{
    "name": "Coop IT Easy Customization",
    "version": "11.0.1.0.0",
    "depends": ["analytic", "project"],
    "author": "Coop IT Easy SCRLfs",
    "license": "AGPL-3",
    "category": "",
    "website": "www.coopiteasy.be",
    "summary": """
        Specifics customizations for Coop IT Easy
    """,
    "description": """
        * reset_so_line on account.analytic.line
        * fields on project.task
        * only display active accounts on activity view
        * sort accounts by line count
    """,
    "data": [
        "data/cron.xml",
        "views/project_view.xml",
        "views/account_analytic.xml",
    ],
    "installable": True,
}
