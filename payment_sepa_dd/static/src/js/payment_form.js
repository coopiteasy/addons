// SPDX-FileCopyrightText: 2024 Coop IT Easy SC
//
// SPDX-License-Identifier: AGPL-3.0-or-later

// From payment_demo/static/src/js/payment_form.js
// From payment_authorize/static/src/js/payment_form.js

odoo.define("payment_sepa_dd.payment_form", (require) => {
    "use strict";

    const checkoutForm = require("payment.checkout_form");
    const manageForm = require("payment.manage_form");

    const sepaDDMixin = {
        /**
         * Return all relevant inline form inputs
         *
         * @private
         * @param {Number} providerId - The id of the selected provider
         * @returns {Object} - An object mapping the name of inline form inputs
         * to their DOM element
         */
        _getInlineFormInputs: function (providerId) {
            return {
                sepa_dd_iban: document.getElementById(`o_sepa_dd_iban_${providerId}`),
                sepa_dd_accept: document.getElementById(
                    `o_sepa_dd_accept_${providerId}`
                ),
            };
        },

        /**
         * Set payment flow as 'direct', because we use an inline form.
         *
         * @private
         * @param {String} code - The code of the selected payment
         * option's provider
         * @param {Number} paymentOptionId - The id of the selected
         * payment option
         * @param {String} flow - The online payment flow of the
         * selected payment option
         * @returns {Promise}
         */
        _prepareInlineForm: function (code, paymentOptionId, flow) {
            if (code !== "sepa_dd") {
                return this._super(...arguments);
            } else if (flow === "token") {
                return Promise.resolve();
            }
            this._setPaymentFlow("direct");
            return Promise.resolve();
        },

        /**
         * Process payment.
         *
         * @private
         * @param {String} code - The code of the provider
         * @param {Number} providerId - The id of the provider handling
         * the transaction
         * @param {Object} processingValues - The processing values of
         * the transaction
         * @returns {Promise}
         */
        _processDirectPayment: function (code, providerId, processingValues) {
            if (code !== "sepa_dd") {
                return this._super(...arguments);
            }

            // First validation of formular
            if (!this._validateFormInputs(providerId)) {
                this._enableButton();
                $("body").unblock();
                return Promise.resolve();
            }

            // Retrieve value from formular
            const inputs = this._getInlineFormInputs(providerId);
            processingValues.sepa_dd_iban = inputs.sepa_dd_iban.value;
            processingValues.sepa_dd_accept = inputs.sepa_dd_accept.value;

            return this._rpc({
                route: "/payment/sepa_dd/process",
                params: processingValues,
            }).then(() => {
                window.location = "/payment/status";
            });
        },

        /**
         * Checks that all payment inputs adhere to the DOM validation
         * constraints.
         *
         * @private
         * @param {Number} providerId - The id of the selected provider
         * @returns {Boolean} - Whether all elements pass the validation
         * constraints
         */
        _validateFormInputs: function (providerId) {
            const inputs = Object.values(this._getInlineFormInputs(providerId));
            return inputs.every((element) => element.reportValidity());
        },
    };

    checkoutForm.include(sepaDDMixin);
    manageForm.include(sepaDDMixin);
});
