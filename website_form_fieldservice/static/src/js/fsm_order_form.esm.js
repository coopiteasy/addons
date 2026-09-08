/* global window, document */

import publicWidget from "@web/legacy/js/public/public_widget";
import {rpc} from "@web/core/network/rpc";

publicWidget.registry.WebsiteFormFieldservice = publicWidget.Widget.extend({
    selector: 'form[data-model_name="fsm.order"]',

    async start() {
        try {
            const result = await rpc("/fsm_orders/get_form_data");
            this._populateBeneficiaries(result.beneficiaries);
            this._populateTypes(result.order_types);

            await this._populateStates();
            const countryEl = this.el.querySelector(
                'select[name="location_country_id"]'
            );
            if (countryEl) {
                countryEl.addEventListener("change", () => {
                    this._populateStates();
                });
            }
        } catch {
            window.location.href =
                "/web/login?redirect=" + encodeURIComponent(window.location.href);
        }
    },

    _populateBeneficiaries(beneficiaries) {
        const selectEl = this.el.querySelector(
            'select[name="social_beneficiary_partner_id"]'
        );
        if (!selectEl) return;
        selectEl.innerHTML = "";
        beneficiaries.forEach((b) => {
            const opt = document.createElement("option");
            opt.value = b.id;
            opt.textContent = b.display_name;
            selectEl.appendChild(opt);
        });
    },

    _populateTypes(order_types) {
        const selectEl = this.el.querySelector('select[name="type"]');
        if (!selectEl) return;
        selectEl.innerHTML = "";
        order_types.forEach((t) => {
            const opt = document.createElement("option");
            opt.value = t.id;
            opt.textContent = t.display_name;
            selectEl.appendChild(opt);
        });
    },

    async _populateStates() {
        const countryEl = this.el.querySelector('select[name="location_country_id"]');
        const stateEl = this.el.querySelector('select[name="location_state_id"]');
        if (!countryEl || !stateEl) return;
        const countryId = countryEl.value;
        if (!countryId) {
            stateEl.innerHTML = "";
            return;
        }
        rpc("/fsm_orders/get_states", {country_id: parseInt(countryId, 10)}).then(
            (result) => {
                stateEl.innerHTML = "";
                result.states.forEach((s) => {
                    const opt = document.createElement("option");
                    opt.value = s.id;
                    opt.textContent = s.display_name;
                    stateEl.appendChild(opt);
                });
            }
        );
    },
});
