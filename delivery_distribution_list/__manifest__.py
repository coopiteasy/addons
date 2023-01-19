{
    "name": "Delivery distribution Management",
    "summary": """
    Manage the distribution of a product through all the deposit points.
    """,
    "author": "Coop IT Easy SC",
    "license": "AGPL-3",
    "version": "14.0.1.0.0",
    "website": "https://coopiteasy.be",
    "category": "Sales",
    "depends": [
        "sale",
        "account",
        "contacts",
    ],
    "data": [
        "security/delivery_distribution_list_security.xml",
        "security/ir.model.access.csv",
        "data/ddl_data.xml",
        "views/partner_view.xml",
        "views/sale_view.xml",
        "views/delivery_distribution_list_view.xml",
        "views/product_view.xml",
        "report/sale_order_report_template.xml",
    ],
}