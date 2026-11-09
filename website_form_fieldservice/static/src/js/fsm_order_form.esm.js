/* global Option, console, document */

import {_t} from "@web/core/l10n/translation";
import publicWidget from "@web/legacy/js/public/public_widget";
import {rpc} from "@web/core/network/rpc";

publicWidget.registry.WebsiteFormFieldservice = publicWidget.Widget.extend({
    selector: 'form[data-model_name="fsm.order"]',

    async start() {
        let data = null;
        try {
            data = await rpc("/fsm_orders/get_form_data");
        } catch (error) {
            console.error(error);
            return;
        }
        this._populateSelect(
            this._getSelect("social_beneficiary_partner_id"),
            data.beneficiaries,
            _t("Select a beneficiary...")
        );
        this._populateSelect(
            this._getSelect("type"),
            data.order_types,
            _t("Select a type...")
        );
        const countrySelect = this._getSelect("location_country_id");
        this._populateSelect(countrySelect, data.countries, _t("Select a country..."));
        if (countrySelect && data.default_country_id) {
            countrySelect.value = data.default_country_id;
        }
        await this._populateStates();
        if (countrySelect) {
            countrySelect.addEventListener("change", () => this._populateStates());
        }
    },

    _getSelect(name) {
        let el = this.el.querySelector(`[name="${name}"]`);
        if (el && el.tagName !== "SELECT") {
            const select = document.createElement("select");
            for (const attr of ["name", "id", "class", "required"]) {
                if (el.hasAttribute(attr)) {
                    select.setAttribute(attr, el.getAttribute(attr));
                }
            }
            el.replaceWith(select);
            el = select;
        }
        return el;
    },

    _populateSelect(select, records, placeholder) {
        if (!select) {
            return;
        }
        select.innerHTML = "";
        if (placeholder) {
            select.add(new Option(placeholder, ""));
        }
        for (const record of records || []) {
            select.add(new Option(record.display_name, record.id));
        }
    },

    async _populateStates() {
        const countrySelect = this.el.querySelector(
            'select[name="location_country_id"]'
        );
        const stateSelect = this._getSelect("location_state_id");
        if (!stateSelect) {
            return;
        }
        stateSelect.removeAttribute("required");
        const countryId =
            countrySelect && countrySelect.value
                ? parseInt(countrySelect.value, 10)
                : false;
        let states = [];
        if (countryId) {
            const result = await rpc("/fsm_orders/get_states", {
                country_id: countryId,
            });
            states = result.states || [];
        }
        this._populateSelect(stateSelect, states, _t("Select a state..."));
    },
});
