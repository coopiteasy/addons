odoo.define("pos_customer_wallet_partner_is_user.PaymentScreen", function (require) {
    "use strict";
    const PaymentScreen = require("point_of_sale.PaymentScreen");

    const Registries = require("point_of_sale.Registries");

    const IsUserPaymentScreen = (PaymentScreen_) =>
        class extends PaymentScreen_ {
            /* eslint-disable no-unused-vars */
            /**
             * Overload function.
             *
             * - If partner hasn't enabled functionality, don't allow wallet payments.
             *
             * @param {Boolean} isForceValidate - Passed to super.
             * @returns {Boolean} Whether the order is valid.
             */
            async validateOrder(isForceValidate) {
                var partner = this.currentOrder.get_partner();
                var [payment_wallet_amount, payment_lines_qty] =
                    this.get_amount_debit_with_customer_wallet_journal();
                var [product_wallet_amount, product_lines_qty] =
                    this.get_amount_credit_with_customer_wallet_product();
                /* eslint-enable no-unused-vars */

                // If the partner is not a customer wallet user, and if a customer
                // wallet operation is being made (via the payment method or via the
                // wallet product), display an error.
                if (
                    (payment_lines_qty || product_lines_qty) &&
                    partner &&
                    !partner.is_customer_wallet_user
                ) {
                    this.showPopup("ErrorPopup", {
                        title: this.env._t("Customer cannot use customer wallet"),
                        body: this.env._t(
                            "Customer has not enabled the usage of a customer wallet. Before the user can use this payment method, they must enable it."
                        ),
                    });
                    return;
                }

                await super.validateOrder(...arguments);
            }
        };

    Registries.Component.extend(PaymentScreen, IsUserPaymentScreen);

    return IsUserPaymentScreen;
});
