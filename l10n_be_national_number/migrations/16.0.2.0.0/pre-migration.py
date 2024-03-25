from openupgradelib import openupgrade

renamed_xml_ids = (
    (
        "l10n_be_national_number.l10n_be_national_number_category",
        "l10n_be_partner_identification.l10n_be_national_registry_number_category",
    ),
)


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.rename_xmlids(env.cr, renamed_xml_ids)
