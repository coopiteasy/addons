# Copyright 2021-Coopdevs Treball SCCL (<https://coopdevs.org>)
# - César López Ramírez - <cesar.lopez@coopdevs.org>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "l10n_es Auto Reload Banks",
    "version": "12.0.1.0.0",
    "depends": ["base", "l10n_es_partner"],
    "author": "Coopdevs Treball SCCL",
    "category": "Accounting & Finance",
    "website": "https://coopdevs.org",
    "license": "AGPL-3",
    "summary": """
        Auto reload Spanish banks from BdE in module upgrade
    """,
    "data": [
        'data/company.xml'
    ],
    "installable": True,
}
