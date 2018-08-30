/*
    POS Round cash Payment line for odoo
    Copyright (C) 2018 Robin Keunen
    @author: Robin Keunen
    The licence is in the file __openerp__.py
*/

odoo.define(
    'pos_round_cash_payment_line.pos_round_cash_payment_line',
    function (require) {

    "use strict";
    var models = require('point_of_sale.models');
    var screens = require('point_of_sale.screens');
    var round_pr = require('web.utils').round_precision;

    var order_prototype = models.Order.prototype;

    models.Order = models.Order.extend({

        round_5c: function(x) {
            return round_pr(x * 20) / 20;
        },

        get_due: function(paymentline) {

            if (!paymentline) {
                var due = this.get_total_with_tax() - this.get_total_paid();
            } else {
                var due = this.get_total_with_tax();
                var lines = this.paymentlines.models;
                for (var i = 0; i < lines.length; i++) {
                    if (lines[i] === paymentline) {
                        break;
                    } else {
                        due -= lines[i].get_amount();
                    }
                }
            }

            if (this.pos.config.cash_rounding_activated
                && paymentline
                && paymentline.cashregister.journal.type === 'cash') {
                return this.round_5c(due);

            } else {
                return round_pr(due, this.pos.currency.rounding)
            }
        },
        // todo check it writes correct journal entries
        get_change: function(paymentline) {
            var change = order_prototype.get_change.call(this, paymentline);
            if (this.pos.config.cash_rounding_activated){
                return this.round_5c(change);
            } else {
                return change;
            }
        },

        add_paymentline: function(cashregister) {
            this.assert_editable();
            var newPaymentline = new models.Paymentline(
                {},
                {
                    order: this,
                    cashregister:cashregister, pos: this.pos
                }
            );
            if(cashregister.journal.type !== 'cash'
                || this.pos.config.iface_precompute_cash) {
                const due = this.get_due(newPaymentline);
                newPaymentline.set_amount( due );
            } else {
                newPaymentline.set_amount( 0 );
            }
            this.paymentlines.add(newPaymentline);
            this.select_paymentline(newPaymentline);
        },

        is_paid: function(){
            if (this.pos.config.cash_rounding_activated
                  && this.is_paid_with_cash()) {
                return Math.abs(this.get_due()) < 0.05;
            } else {
                return this.get_due() === 0;
            }
        },

        add_round_line: function (remainder) {
            var remainder_product = this.pos.db.get_product_by_id(
                this.pos.config.round_remainder_product_id[0]
            );
            var lines = this.get_orderlines();

            for (var i = 0; i < lines.length; i++) {
                if (lines[i].get_product() === remainder_product) {
                    lines[i].set_unit_price(remainder);
                    return;
                }
            }
            this.add_product(remainder_product, {quantity: 1, price: remainder});
        }
    });

    screens.PaymentScreenWidget.include({
        finalize_validation: function () {
            var order = this.pos.get_order();
            if (this.pos.config.cash_rounding_activated
                    && Math.abs(order.get_due()) < 0.5 ) {
                order.add_round_line(-order.get_due());
            }
            return this._super()
        }
    });
});
