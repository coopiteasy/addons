odoo.define("pos_customer_wallet_partner_is_user.screens", function (require) {
    "use strict";
    var core = require("web.core");
    var screens = require("point_of_sale.screens");

    var _t = core._t;

    screens.PaymentScreenWidget.include({
        /**
         * Overload function.
         *
         * - If client hasn't enabled functionality, don't allow wallet payments.
         */
        order_is_valid: function (force_validation) {
            if (!this._super(force_validation)) {
                return false;
            }

            var client = this.pos.get_client();
            var [payment_wallet_amount, payment_lines_qty] =
                this.get_amount_debit_with_customer_wallet_journal();
            var [product_wallet_amount, product_lines_qty] =
                this.get_amount_credit_with_customer_wallet_product();

            // If the client is not a customer wallet user, and if a customer
            // wallet operation is being made (via the payment method or via the
            // wallet product), display an error.
            if (
                (payment_lines_qty || product_lines_qty) &&
                client &&
                !client.is_customer_wallet_user
            ) {
                this.gui.show_popup("error", {
                    title: _t("Customer cannot use customer wallet"),
                    body: _t(
                        "Customer has not enabled the usage of a customer wallet. Before the user can use this payment method, they must enable it."
                    ),
                });
                return false;
            }
            return true;
        },
    });
});
