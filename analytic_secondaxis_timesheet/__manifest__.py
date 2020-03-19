# Copyright 2010 Camptocamp SA (http://www.camptocamp.com)
#   Joel Grand-guillaume (Camptocamp)
# Copyright 2015-2020 Coop IT Easy SCRLfs (http://coopiteasy.be)
#   Houssine Bakkali <houssine@coopiteasy.be>
#   Rémy Taymans <remy@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Timesheet Analytic Second Axis",
    "version": "12.0.1.0.0",
    "author": "Camptocamp, "
    "Coop IT Easy SCRLfs, "
    "Odoo Community Association (OCA)",
    "category": "Generic Modules/Accounting",
    "description": """
    Add a second analytical axis on analytic lines allowing you to make
    reporting on.

    This module allow you to make cross-reporting between those two
    axes, like all analytic lines that concern for example : The
    activity "Communication" and the project "Product 1 Integration".

    This second axis is called "activities" and you will be able to define for
    each analytical account, what are the allowed activities for it.

    This module enables the second axis on timesheet.
    """,
    "website": "http://coopiteasy.be",
    "license": "AGPL-3",
    "depends": ["analytic_secondaxis", "hr_timesheet"],
    "data": ["views/hr_timesheet.xml"],
}
