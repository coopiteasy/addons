odoo.define("pos_customer_wallet.models", function (require) {
    "use strict";

    const {Order} = require("point_of_sale.models");
    const Registries = require("point_of_sale.Registries");

    const WalletOrder = (Order_) =>
        class extends Order_ {
            export_for_printing() {
                var json = super.export_for_printing(...arguments);
                json.customer_wallet_balance = this.partner
                    ? this.partner.customer_wallet_balance
                    : 0;
                return json;
            }
        };

    Registries.Model.extend(Order, WalletOrder);
});
