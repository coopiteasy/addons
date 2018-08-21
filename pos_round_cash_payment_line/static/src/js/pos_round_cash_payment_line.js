/*
    POS Round cash Payment line for odoo
    Copyright (C) 2018 Robin Keunen
    @author: Robin Keunen
    The licence is in the file __openerp__.py
*/

odoo.define('pos_round_cash_payment_line.pos_round_cash_payment_line', function (require) {
    "use strict";
    var models = require('point_of_sale.models');
    var round_pr = require('web.utils').round_precision;

    var order_prototype = models.Order.prototype;
    var psw_prototype = models.PaymentScreenWidget.prototype;

    models.Order = models.Order.extend({

        round_5c: function(x) {
            return round_pr(x * 20) / 20;
        },

        round_5c_remainder: function(x) {
            var rounded_value = round_pr(x * 20) / 20;
            return rounded_value - x;
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

            if (paymentline && paymentline.cashregister.journal.type === 'cash') {
                return this.round_5c(due);  // fixme swiss parameter

            } else {
                return round_pr(due, this.pos.currency.rounding)
            }
        },


        get_change: function(paymentline) {
            var change = order_prototype.get_change.call(this, paymentline);
            return this.round_5c(change);  // fixme swiss parameter
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
            if (this.is_paid_with_cash()) {  // fixme swiss parameter
                return Math.abs(this.get_due()) < 0.05;
            } else {
                return this.get_due() === 0;
            }
        },
    });

    models.PaymentScreenWidget = models.PaymentScreenWidget.extend({
        finalize_validation: function () {
            var order = this.pos.get_order();
            if ( Math.abs(order.get_due()) < 0.5 ) {  // fixme swiss parameter
                // add line
            }
            psw_prototype.finalize_validation.call(this)
        }
    });
});
