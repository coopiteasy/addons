from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    for id_numbers in env["res.partner"].search([]).mapped("id_numbers"):
        if id_numbers.category_id == env.ref(
            "l10n_be_national_number.l10n_be_national_number_category"
        ):
            id_numbers.category_id = env.ref(
                "l10n_be_partner_identification.l10n_be_national_registry_number_category"
            ).id
