/*
    POS Round cash Payment for odoo
    Copyright (C) 2018 Coop IT Easy SCRLfs
    @author: Robin Keunen
    @author: Houssine BAKKALI
    The licence is in the file __manifest__.py
*/

odoo.define(
    'pos_round_cash_payment.pos_round_cash_payment_line',
    function (require) {

        "use strict";
        var models = require('point_of_sale.models');
        var screens = require('point_of_sale.screens');
        var round_pr = require('web.utils').round_precision;

        var order_prototype = models.Order.prototype;

        models.load_fields('account.journal', 'cash_rounding');

        models.Order = models.Order.extend({

            round_5c: function (x) {
                return round_pr(x * 20) / 20;
            },

            round_5c_remainder: function (x) {
                return x - this.round_5c(x);
            },

            add_remainder_line: function (cashregister) {
                this.assert_editable();
                const due = this.get_due(newPaymentline);
                const remainder = this.round_5c_remainder(due)
                if (remainder !== 0) {
                    var newPaymentline = new models.Paymentline({},
                        {
                            order: this,
                            cashregister: cashregister, pos: this.pos
                        }
                    );

                    newPaymentline.set_amount(remainder);
                    this.paymentlines.add(newPaymentline);
                    this.select_paymentline(newPaymentline);
                }
            },
        });

        screens.PaymentScreenWidget.include({
            click_paymentmethods: function (id) {
                var cashregister = null;

                for (var i = 0; i < this.pos.cashregisters.length; i++) {
                    if (this.pos.cashregisters[i].journal_id[0] === id) {
                        cashregister = this.pos.cashregisters[i];
                        break;
                    }
                }

                if (cashregister.journal.cash_rounding == false) {
                    if (this.pos.config.cash_rounding_activated && cashregister.journal.type == 'cash') {
                        var rounding_cashregister = null;
                        for (var i = 0; i < this.pos.cashregisters.length; i++) {
                            if (this.pos.cashregisters[i].journal.cash_rounding === true) {
                                rounding_cashregister = this.pos.cashregisters[i];
                                break;
                            }
                        }
                        this.pos.get_order().add_remainder_line(rounding_cashregister);
                    }
                    this._super.apply(this, arguments);
                }
            },
        });
    });
