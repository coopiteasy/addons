# Copyright 2010 Camptocamp SA (http://www.camptocamp.com)
#   Joel Grand-guillaume (Camptocamp)
# Copyright 2015-2020 Coop IT Easy SCRLfs (http://coopiteasy.be)
#   Houssine Bakkali <houssine@coopiteasy.be>
#   Rémy Taymans <remy@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Account Analytic Second Axis",
    "version": "12.0.1.0.0",
    "author": "Camptocamp, "
    "Coop IT Easy SCRLfs, "
    "Odoo Community Association (OCA)",
    "category": "Generic Modules/Accounting",
    "description": """
    Add a second analytical axis on analytic lines allowing you to make
    reporting on.

    This module allow you to make cross-reporting between those two
    axes, like all analytic lines that concern for example:
    The activity "Communication" and the project "Product 1 Integration".

    This second axis is called "activities" and you will be able to define for
    each analytical account, what are the allowed activities for it.

    There's also a kind of heritage between analytical account. Adding
    activities on parent account will allow child to benefit from. So
    you can define a set of activities for each parent analytic account
    like:

    Administratif
        - Intern
        - Project 1
    Customers project
        - Project X
        - Project Y

    What will be true for Administratif, will be true for Intern too.
    """,
    "website": "http://coopiteasy.be",
    "license": "AGPL-3",
    "depends": ["account", "analytic", "account_analytic_parent"],
    "demo": ["data/analytic_secondaxis_demo.xml"],
    "data": [
        "security/ir.model.access.csv",
        "views/analytic_activity.xml",
        "views/analytic_account.xml",
    ],
}
