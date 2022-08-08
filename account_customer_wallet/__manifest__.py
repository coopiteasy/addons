# Copyright 2022 Coop IT Easy SC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Account Customer Wallet",
    "summary": """
        Allow customers to pay using a wallet which is tracked by the company.""",
    "version": "12.0.1.2.0",
    "category": "Accounting & Finance",
    "website": "https://coopiteasy.be",
    "author": "Coop IT Easy SC",
    "license": "AGPL-3",
    "application": False,
    "depends": [
        "account",
    ],
    "excludes": [],
    "data": [
        "views/account_journal_views.xml",
        "views/account_payment_views.xml",
        "views/product_template_views.xml",
        "views/res_config_settings_views.xml",
        "views/res_partner_views.xml",
    ],
    "demo": [
        "demo/account_account_demo.xml",
        "demo/account_journal_demo.xml",
        "demo/product_product_demo.xml",
        "demo/res_company_demo.xml",
    ],
    "qweb": [],
}
