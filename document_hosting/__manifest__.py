# Copyright 2018 - Today Coop IT Easy SCRLfs (<http://www.coopiteasy.be>)
# - Rémy Taymans <remy@coopiteasy.be>
# - Elouan Le bars <elouan@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Document Hosting",
    "summary": """
    Manage documents that can be published on website with document_hosting_website.
    """,
    "description": """
    """,
    "author": "Coop IT Easy SCRLfs",
    "license": "AGPL-3",
    "version": "12.0.1.0.0",
    "website": "www.coopiteasy.be",
    "category": "Document",
    "depends": ["base", "web", "mail",],
    "data": [
        "security/ir.model.access.csv",
        "views/document_hosting_menu.xml",
        "views/document_hosting_views.xml",
    ],
}
