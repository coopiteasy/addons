# Copyright 2018 - Today Coop IT Easy SC (<http://www.coopiteasy.be>)
# - Rémy Taymans <remy@coopiteasy.be>
# - Elouan Le bars <elouan@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Document Hosting",
    "summary": """
    Manage documents that can be published on website with ??.
    """,
    "author": "Coop IT Easy SC",
    "license": "AGPL-3",
    "version": "12.0.1.0.0",
    "website": "https://coopiteasy.be",
    "category": "Document",
    "depends": ["base", "web", "website", "mail"],
    "data": [
        "security/ir.model.access.csv",
        "views/document_hosting_menu.xml",
        "views/document_hosting_views.xml",
        "views/document_hosting_website_templates.xml",
        "views/res_config_settings_views.xml",
    ],
}
