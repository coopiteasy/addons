{
    'name': "PoS order email",
    'summary': """
        Module that adds the option to send an order by email
    """,

    'description': """
        Long description of module's purpose
    """,
    'author': "Coop IT Easy SCRLfs",
    'website': "https://www.coopiteasy.be",
    'category': 'Point Of Sale',
    'version': '12.0.1.0.0',
    'depends': ['beesdoo_base', 'beesdoo_product'],
    'data': [
        'data/email.xml',
    ],
    'qweb': ['static/src/xml/templates.xml'],
}

