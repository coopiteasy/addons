/** @odoo-module alias=pos_customer_wallet.PaymentScreen **/
// SPDX-FileCopyrightText: 2022 Coop IT Easy SC
//
// SPDX-License-Identifier: AGPL-3.0-or-later

import PaymentScreen from "point_of_sale.PaymentScreen";

import Registries from "point_of_sale.Registries";

const WalletPaymentScreen = (PaymentScreen_) =>
    class extends PaymentScreen_ {
        /* eslint-disable no-unused-vars */
        /**
         * Overload function.
         *
         * - If wallet journal is selected, check if customer is selected.
         * - if wallet journal is selected, check if wallet amount is sufficient.
         *
         * @param {Boolean} isForceValidate - Passed to super.
         * @returns {Boolean} Whether the order is valid.
         */
        async validateOrder(isForceValidate) {
            /* eslint-enable no-unused-vars */
            var partner = this.currentOrder.get_partner();
            var [payment_wallet_amount, payment_lines_qty] =
                this.get_amount_debit_with_customer_wallet_journal();
            var [product_wallet_amount, product_lines_qty] =
                this.get_amount_credit_with_customer_wallet_product();

            var wallet_amount = payment_wallet_amount - product_wallet_amount;

            if (!partner) {
                if (payment_lines_qty > 0) {
                    this.showPopup("ErrorPopup", {
                        title: this.env._t("No customer selected"),
                        body: this.env._t(
                            "Cannot use customer wallet payment method without selecting a customer.\n\n Please select a customer or use a different payment method."
                        ),
                    });
                    return;
                }
                if (product_lines_qty > 0) {
                    var wallet_product_names = [];
                    var wallet_products = this.find_customer_wallet_products();
                    wallet_products.forEach(function (product) {
                        wallet_product_names.push(product.display_name);
                    });
                    this.showPopup("ErrorPopup", {
                        title: this.env._t("No customer selected"),
                        body:
                            this.env._t("Cannot sell the product '") +
                            wallet_product_names.join(",") +
                            this.env._t(
                                "' without selecting a customer. Please select a customer or remove the order line(s)."
                            ),
                    });
                    return;
                }
            } else if (this.is_balance_above_minimum(partner, wallet_amount)) {
                this.showPopup("ErrorPopup", {
                    title: this.env._t("Customer wallet balance not sufficient"),
                    body: this.env._t(
                        "There is not enough balance in the customer's wallet to perform this order."
                    ),
                });
                return;
            }

            await super.validateOrder(...arguments);
        }

        /**
         * Overload function.
         *
         * Once the order is validated, update the wallet amount
         * of the current customer, if defined.
         */
        async _finalizeValidation() {
            var partner = this.currentOrder.get_partner();
            if (partner) {
                var payment_wallet_amount =
                    this.get_amount_debit_with_customer_wallet_journal()[0];
                var product_wallet_amount =
                    this.get_amount_credit_with_customer_wallet_product()[0];
                var wallet_amount = payment_wallet_amount - product_wallet_amount;
                partner.customer_wallet_balance -= wallet_amount;
            }

            await super._finalizeValidation();
        }

        is_balance_above_minimum(client, wallet_amount) {
            return (
                client.customer_wallet_balance - wallet_amount <=
                this.env.pos.config.minimum_wallet_amount - 0.00001
            );
        }

        /**
         * Calculate the balance of the customer wallet after completing this
         * order.
         *
         * @returns {Number} New balance.
         */
        get new_wallet_amount() {
            var partner = this.currentOrder.get_partner();
            if (partner) {
                var payment_wallet_amount =
                    this.get_amount_debit_with_customer_wallet_journal()[0];
                var product_wallet_amount =
                    this.get_amount_credit_with_customer_wallet_product()[0];
                return (
                    partner.customer_wallet_balance -
                    payment_wallet_amount +
                    product_wallet_amount
                );
            }
            return false;
        }

        /**
         * Return the payment method of the wallet journal, if exists.
         *
         * @returns A payment method which has a customer
         * wallet journal. The first match is returned.
         */
        find_customer_wallet_payment_method() {
            // This is fairly naive.
            for (var i = 0; i < this.payment_methods_from_config.length; i++) {
                if (this.payment_methods_from_config[i].is_customer_wallet_method) {
                    return this.payment_methods_from_config[i];
                }
            }
            return null;
        }

        /**
         * Return the wallet products, if exist.
         *
         * @returns {list} A list of products which are marked as wallet
         * products.
         */
        find_customer_wallet_products() {
            var wallet_products = [];
            for (const value of Object.values(this.env.pos.db.product_by_id)) {
                if (value.is_customer_wallet_product) {
                    wallet_products.push(value);
                }
            }
            return wallet_products;
        }

        /**
         * Return the payment amount with wallet payment method.
         *
         * @returns {list} A list of two elements. The first element is the
         * balance of payment done with wallet payment method. The second
         * element is the number of payment lines.
         */
        get_amount_debit_with_customer_wallet_journal() {
            var order = this.currentOrder;
            var method = this.find_customer_wallet_payment_method();
            var wallet_amount = 0;
            var lines_qty = 0;
            order.paymentlines.forEach((item) => {
                if (item.payment_method === method) {
                    wallet_amount += item.amount;
                    lines_qty += 1;
                }
            });
            return [wallet_amount, lines_qty];
        }

        /**
         * Return the amount credited by wallet products.
         *
         * @returns {list} A list of two elements. The first element is the
         * balance of order lines done with wallet product. The second element
         * is the number of order lines.
         */
        get_amount_credit_with_customer_wallet_product() {
            var order = this.currentOrder;
            var wallet_product_ids = [];
            var wallet_products = this.find_customer_wallet_products();
            wallet_products.forEach(function (product) {
                wallet_product_ids.push(product.id);
            });
            var wallet_amount = 0;
            var lines_qty = 0;

            order.orderlines.forEach((orderline) => {
                if (wallet_product_ids.includes(orderline.product.id)) {
                    wallet_amount += orderline.get_price_without_tax();
                    lines_qty += 1;
                }
            });

            return [wallet_amount, lines_qty];
        }
    };

Registries.Component.extend(PaymentScreen, WalletPaymentScreen);
export default WalletPaymentScreen;
