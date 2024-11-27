odoo.define("website_sale_sepa_dd_payment.payment_form", (require) => {
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
         * Return values to pass to the default transaction validation
         * route
         *
         * @private
         * @param {String} code - The code of the payment option's provider
         * @param {Number} paymentOptionId - The id of the selected provider
         * @param {String} flow - The online payment flow of the transaction
         * @returns {Object} - The params for the default transaction route
         */
        _prepareTransactionRouteParams: function (code, paymentOptionId, flow) {
            const values = this._super(code, paymentOptionId, flow);
            const inputs = this._getInlineFormInputs(paymentOptionId);
            values.sepa_dd_iban = inputs.sepa_dd_iban.value;
            values.sepa_dd_accept = inputs.sepa_dd_accept.value;
            return values;
        },

        /**
         * Ensure that inputs for the form are valid (more validation
         * are done in python by the backend).
         *
         * @override method from payment.payment_form_mixin
         * @private
         * @param {String} code - The code of the payment option's provider
         * @param {Number} paymentOptionId - The id of the payment option handling the transaction
         * @param {String} flow - The online payment flow of the transaction
         * @returns {Promise}
         */
        _processPayment: function (code, paymentOptionId, flow) {
            if (code !== "custom" || flow === "token") {
                return this._super(...arguments);
            }

            if (!this._validateFormInputs(paymentOptionId)) {
                this._enableButton();
                $("body").unblock();
                return Promise.resolve();
            }

            return this._super(...arguments);
        },

        /**
         * Checks that all payment inputs adhere to the DOM validation constraints.
         *
         * @private
         * @param {Number} providerId - The id of the selected provider
         * @returns {Boolean} - Whether all elements pass the validation constraints
         */
        _validateFormInputs: function (providerId) {
            const inputs = Object.values(this._getInlineFormInputs(providerId));
            return inputs.every((element) => element.reportValidity());
        },
    };

    checkoutForm.include(sepaDDMixin);
    manageForm.include(sepaDDMixin);
});
