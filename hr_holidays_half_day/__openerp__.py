# -*- coding: utf-8 -*-
# Copyright 2019 Coop IT Easy SCRLfs
#   - Vincent Van Rossem <vincent@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "HR Holidays Half/Full Day",
    "version": "9.0.1.0.0",
    "category": "Human Resources",
    "summary": """Computes Leaves Request in half or full days according to employee's contracts""",
    "author": "Coop IT Easy SCRLfs, Odoo Community Association (OCA)",
    "website": "www.coopiteasy.be",
    "license": "AGPL-3",
    "depends": ["hr_holidays", "hr_contract", "web_readonly_bypass"],
    "data": ["views/hr_holidays_view.xml", "views/company_view.xml"],
    "demo": [],
    "installable": True,
}
