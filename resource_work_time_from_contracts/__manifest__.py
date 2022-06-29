# Copyright 2021 Coop IT Easy SC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Resource Work Time From Contracts",
    "summary": (
        "Take the contracts of an employee into account when computing work "
        "time per day"
    ),
    "version": "12.0.1.0.0",
    "license": "AGPL-3",
    "author": "Coop IT Easy SC",
    "website": "https://coopiteasy.be",
    "category": "Human Resources",
    "depends": [
        "hr_contract",
    ],
    "data": [
        "views/hr_employee.xml",
        "views/resource_resource.xml",
    ],
    "demo": [],
}
