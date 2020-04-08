# Copyright 2020-      Coop IT Easy SCRLfs (<http://www.coopiteasy.be>)
# - Manuel Claeys Bouuaert - <manuel@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'Portal Partner ISR',
    'version': '11.0.1.0.0',
    'author': 'Coop IT Easy SCRLfs',
    'category': 'Website',
    'website': 'https://www.coopiteasy.be',
    'license': 'AGPL-3',
    'description': """
    This module adds a button on the client portal to an externally generated ISR slip. 
    """,
    'depends': [
        'portal',
        'partner_isr',
        'distribution_circuits_website_sale',
    ],
    'data': [
        'views/partner_isr.xml'
    ],
    'installable': True,
}
