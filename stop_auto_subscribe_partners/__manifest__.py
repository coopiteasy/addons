##############################################################################
#
#
#    Part of cube48.de.
#
#
##############################################################################
{
    "name": "Stop Auto Subscribe Partners",
    "summary": """
        New partners will not become auto followers any longer.""",
    "description": """
        New partners will not become auto followers any longer.
    """,
    "author": "cube48 AG, Coop IT Easy SC",
    "website": "https://coopiteasy.be",
    "category": "Tools",
    "version": "12.0.1.0.0",
    "depends": ["base", "mail", "base_setup"],
    "data": [
        "views/views.xml",
    ],
    "images": ["static/description/banner.png"],
    "license": "AGPL-3",
    "installable": True,
}
