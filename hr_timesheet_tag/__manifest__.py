# Copyright 2020 Coop IT Easy SCRLfs (http://coopiteasy.be)
#   Rémy Taymans <remy@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Hr Timesheet Tag',
    'description': """
        Tag your timesheet activity.""",
    'version': '12.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'Coop IT Easy SCRLfs',
    'website': 'http://coopiteasy.be',
    'depends': [
        "hr_timesheet"
    ],
    'data': [
        "views/hr_timesheet.xml",
    ],
    'demo': [
    ],
}
