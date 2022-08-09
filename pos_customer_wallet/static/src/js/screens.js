odoo.define("pos_customer_wallet.screens", function (require) {
    "use strict";
    var core = require("web.core");
    var screens = require("point_of_sale.screens");

    var _t = core._t;

    screens.PaymentScreenWidget.include({
        /**
         * Overload function.
         *
         * Update balance wallet amount when customer changed.
         */
        customer_changed: function () {
            this._super();
            if (this.pos.config.is_enabled_customer_wallet) {
                var client = this.pos.get_client();
                this.$(".balance").text(
                    client ? this.format_currency(client.customer_wallet_balance) : ""
                );
                this.$(".balance-header").text(
                    client ? _t("Customer Wallet Balance") : ""
                );
            }
        },

        /**
         * Overload function.
         *
         * - If wallet journal is selected, check if customer is selected.
         * - if wallet journal is selected, check if wallet amount is sufficient.
         */
        order_is_valid: function () {
            if (!this._super()) {
                return false;
            }

            var client = this.pos.get_client();
            var [payment_wallet_amount, payment_lines_qty] =
                this.get_amount_debit_with_customer_wallet_journal();

            var [product_wallet_amount, product_lines_qty] =
                this.get_amount_credit_with_customer_wallet_product();

            var wallet_amount = payment_wallet_amount - product_wallet_amount;

            if (!client) {
                if (payment_lines_qty > 0) {
                    this.gui.show_popup("error", {
                        title: _t("No customer selected"),
                        body: _t(
                            "Cannot use customer wallet payment method without selecting a customer.\n\n Please select a customer or use a different payment method."
                        ),
                    });
                    return false;
                }
                if (product_lines_qty > 0) {
                    var wallet_product_names = [];
                    var wallet_products = this.find_customer_wallet_products();
                    wallet_products.forEach(function (product) {
                        wallet_product_names.push(product.display_name);
                    });
                    this.gui.show_popup("error", {
                        title: _t("No customer selected"),
                        body:
                            _t("Cannot sell the product '") +
                            wallet_product_names.join(",") +
                            _t(
                                "' without selecting a customer. Please select a customer or remove the order line(s)."
                            ),
                    });
                    return false;
                }
            } else {
                if (client.customer_wallet_balance - wallet_amount <= -0.00001) {
                    this.gui.show_popup("error", {
                        title: _t("Customer wallet balance not sufficient"),
                        body: _t(
                            "There is not enough balance in the customer's wallet to perform this order."
                        ),
                    });
                    return false;
                }
            }

            return true;
        },

        /**
         * Overload function.
         *
         * Once the order is validated, update the wallet amount
         * of the current customer, if defined.
         */
        finalize_validation: function () {
            var [payment_wallet_amount, _] =
                this.get_amount_debit_with_customer_wallet_journal();
            var [product_wallet_amount, _] =
                this.get_amount_credit_with_customer_wallet_product();
            var wallet_amount = payment_wallet_amount - product_wallet_amount;

            var client = this.pos.get_client();

            if (client) {
                client.customer_wallet_balance -= wallet_amount;
            }

            this._super();
        },

        /**
         * Return the payment method of the wallet journal, if exists.
         *
         */
        find_customer_wallet_payment_method() {
            // This is fairly naive.
            for (var i = 0; i < this.pos.cashregisters.length; i++) {
                if (this.pos.cashregisters[i].journal.is_customer_wallet_journal) {
                    return this.pos.cashregisters[i];
                }
            }
            return null;
        },

        /**
         * Return the wallet products, if exist.
         *
         */
        find_customer_wallet_products() {
            var self = this;
            var wallet_products = [];
            Object.keys(this.pos.db.product_by_id).forEach(function (key) {
                if (self.pos.db.product_by_id[key].is_customer_wallet_product) {
                    wallet_products.push(self.pos.db.product_by_id[key]);
                }
            });
            return wallet_products;
        },

        /**
         * Return the payment amount with wallet journals.
         *
         * @return {wallet_total, lines_qty}
         *  - wallet_total is the balance of payment done with wallet journal
         *  - lines_qty is the number of payment lines
         */
        get_amount_debit_with_customer_wallet_journal() {
            var order = this.pos.get_order();
            var cashregister = this.find_customer_wallet_payment_method();
            var wallet_amount = 0;
            var lines_qty = 0;
            var lines = order.paymentlines.models;
            for (var i = 0; i < lines.length; i++) {
                if (lines[i].cashregister === cashregister) {
                    wallet_amount += lines[i].amount;
                    lines_qty += 1;
                }
            }
            return [wallet_amount, lines_qty];
        },

        /**
         * Return the amount credited by wallet products.
         *
         * @return {wallet_total, lines_qty}
         *  - wallet_total is the balance of order lines done with wallet product
         *  - lines_qty is the number of order lines
         */
        get_amount_credit_with_customer_wallet_product() {
            var order = this.pos.get_order();
            var wallet_product_ids = [];
            var wallet_products = this.find_customer_wallet_products();
            wallet_products.forEach(function (product) {
                wallet_product_ids.push(product.id);
            });
            var wallet_amount = 0;
            var lines_qty = 0;

            order.orderlines.forEach(function (orderline) {
                if (wallet_product_ids.includes(orderline.product.id)) {
                    wallet_amount += orderline.get_price_without_tax();
                    lines_qty += 1;
                }
            });

            return [wallet_amount, lines_qty];
        },
    });
});
