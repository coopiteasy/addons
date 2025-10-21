# Copyright 2023 Akretion (http://www.akretion.com).
# @author Olivier Nibart <olivier.nibart@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "HR PoS Config",
    "summary": """Add an pos_config_ids to the Employee model
    to allow a PoS user that have sufficient rights on the Employees
    to give them access to one or more PoS.""",
    "version": "16.0.0.0.1",
    "author": "Akretion",  # pylint: disable=manifest-required-author
    "website": "https://github.com/coopiteasy/addons",
    "license": "AGPL-3",
    "category": "Point Of Sale",
    "depends": [
        "pos_hr",
    ],
    "data": [
        "views/hr_employee_views.xml",
    ],
    "installable": True,
    "application": False,
}
