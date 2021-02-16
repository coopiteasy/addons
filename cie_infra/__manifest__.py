# -*- coding: utf-8 -*-
{
    'name': "cie_infra",

    'summary': """
        this module allows to visualize our servers throught an inventary. """,

    'description': """
        The purpose of this module is to visualize all the information
	contains on our server. It means the datacenter, the location,
	the different instance on it and finally the different module.
    """,

    'author': "CoopItEasy/EliotVanGoethem",
    'website': "http://coopiteasy.be",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    #'category': 'Uncategorized',
    #'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
	'security/cie_infra_security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/cie_infra_server_views.xml',
        'views/cie_infra_instance_view.xml'
    ],
    # only loaded in demonstration mode
    #'demo': [
    #    'demo/demo.xml',
    #],
}
