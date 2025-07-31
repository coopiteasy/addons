from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    old_id = env.ref("l10n_be_national_number.l10n_be_national_number_category").id
    new_id = env.ref(
        "l10n_be_partner_identification.l10n_be_national_registry_number_category"
    ).id
    id_numbers = (
        env["res.partner.id_number"]
        .with_context(active_test=False)
        .search([("category_id", "=", old_id)])
    )
    id_numbers.write({"category_id": new_id})
