# -*- coding: utf-8 -*-
# © 2017- Houssine BAKKALI - Coop IT Easy SCRLfs
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


{
    'name': 'Website Event Attendance',
    'version': '1.0',
    'category': 'Website',
    'sequence': 95,
    'author': "Houssine BAKKALI - Coop IT Easy SCRLfs",
    'summary': 'Display the subscribed people to an event',
    'description': """

============================

This module allows get the attendance to an event without having to log in.
The link will contains a token allowing to identify the event and the display 
the registered people and there status.

    """,
    'depends': ['website_event'],
    'data': [
        'views/event_templates.xml',
        'views/event_views.xml',
    ],
    'installable': True,
}
