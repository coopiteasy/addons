{
    'name': 'Add To Cart',
    'category': 'Website',
    'summary': 'Sell Your Products Online with ease.',
    'website': 'https://www.coopiteasy.be',
    'version': '1.0',
    'description': """
Odoo E-Commerce
==================

    """,
	'author': ['TechHighway Systems Pvt. Ltd.',
              'Houssine BAKKALI, Coop IT Easy SCRLfs'],
    'depends': ['website','website_sale'],
	'data': [
        'views/add_to_cart_template_view.xml',
    ],
	'images': ['static/description/add2cart_prod_kanban_view.png'],	 
	'installable': True,
	'application': True,
}
