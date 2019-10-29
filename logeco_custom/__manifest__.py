# Copyright 2019 Coop IT Easy SCRL fs
#   Manuel Claeys Bouuaert <manuel@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Housing Cooperative Custom",
    "summary": "Custom settings for swiss housing cooperative",
    "author": "Coop IT Easy SCRL",
    "website": "https://coopiteasy.be",
    "category": "Uncategorized",
    "version": "12.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["housing_cooperative_base", "l10n_ch_states"],
    "data": ["data/data.xml", "views/building.xml", "views/housing.xml"],
    "installable": True,
    "application": False,
}
