# Copyright 2017 Tecnativa - Luis M. Ontalba
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Contract timesheet monitoring",
    "summary": "Compute time spent on service contracts",
    "version": "16.0.1.0.0",
    "category": "Sales",
    "author": "Coop IT Easy SC, Odoo Community Association (OCA)",
    "website": "https://github.com/coopiteasy/addons",
    "depends": ["contract", "hr_timesheet"],
    "development_status": "Production/Stable",
    "data": [
        "views/contract.xml",
        "views/contract_portal_templates.xml",
    ],
    "license": "AGPL-3",
    "installable": True,
}
