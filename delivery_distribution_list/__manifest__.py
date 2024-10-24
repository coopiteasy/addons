{
    "name": "Delivery distribution Management",
    "summary": """
    Manage the distribution of a product through all the deposit points.
    """,
    "author": "Coop IT Easy SC",
    "license": "AGPL-3",
    "version": "16.0.1.0.0",
    "website": "https://github.com/coopiteasy/addons",
    "category": "Sales",
    "depends": [
        "sale_management",
        "account",
    ],
    "data": [
        "security/delivery_distribution_list_security.xml",
        "security/ir.model.access.csv",
        "data/ddl_data.xml",
        "views/delivery_distribution_list_view.xml",
        "views/partner_view.xml",
        "views/sale_view.xml",
    ],
    "assets": {
        "web.assets_qweb": [
            "report/sale_order_report_template.xml",
        ],
    },
}
