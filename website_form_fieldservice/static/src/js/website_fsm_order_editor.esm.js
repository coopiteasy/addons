import FormEditorRegistry from "@website/js/form_editor_registry";
import {_t} from "@web/core/l10n/translation";

FormEditorRegistry.add("create_fsm_order", {
    formFields: [
        {
            name: "social_beneficiary_partner_id",
            type: "many2one",
            required: true,
            relation: "res.partner",
            records: [],
            string: _t("Beneficiary"),
        },
        {
            name: "location_name",
            type: "char",
            custom: true,
            required: true,
            string: _t("Location Name"),
        },
        {
            name: "location_street",
            type: "char",
            custom: true,
            required: true,
            string: _t("Street"),
        },
        {
            name: "location_street2",
            type: "char",
            custom: true,
            string: _t("Street 2"),
        },
        {
            name: "location_zip",
            type: "char",
            custom: true,
            required: true,
            string: _t("Zip"),
        },
        {
            name: "location_city",
            type: "char",
            custom: true,
            required: true,
            string: _t("City"),
        },
        {
            name: "location_country_id",
            type: "many2one",
            custom: true,
            required: true,
            relation: "res.country",
            records: [],
            string: _t("Country"),
        },
        {
            name: "location_state_id",
            type: "many2one",
            custom: true,
            relation: "res.country.state",
            records: [],
            string: _t("State"),
        },
        {
            name: "scheduled_date_start",
            type: "datetime",
            string: _t("Scheduled Date Start"),
        },
        {
            name: "scheduled_duration",
            type: "float",
            string: _t("Scheduled Duration In Hours"),
        },
        {
            name: "type",
            type: "many2one",
            relation: "fsm.order.type",
            records: [],
            string: _t("Type"),
        },
        {
            name: "description",
            type: "text",
            required: true,
            string: _t("Description"),
        },
        {
            name: "resolution",
            type: "text",
            string: _t("Resolution"),
        },
    ],
});
