# Copyright 2021 Coop IT Easy SC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Subscription Web Access",
    "summary": "Compute whether a partner has ongoing contracts",
    "version": "16.0.1.0.1",
    "license": "AGPL-3",
    "author": "Coop IT Easy SC",
    "website": "https://github.com/coopiteasy/addons",
    "depends": [
        "contract",
        "website_sale_product_trial",
    ],
    "data": [
        "data/subscription_status_cron.xml",
        "views/res_partner.xml",
    ],
}
