// SPDX-FileCopyrightText: 2022 Coop IT Easy SC
//
// SPDX-License-Identifier: AGPL-3.0-or-later
odoo.define("pos_customer_wallet_partner_is_user.models", function (require) {
    "use strict";

    const {Order} = require("point_of_sale.models");
    const Registries = require("point_of_sale.Registries");

    const WalletOrder = (Order_) =>
        class extends Order_ {
            export_for_printing() {
                var json = super.export_for_printing(...arguments);
                json.is_customer_wallet_user = this.partner.is_customer_wallet_user
                    ? this.partner
                    : false;
                return json;
            }
        };

    Registries.Model.extend(Order, WalletOrder);
});
