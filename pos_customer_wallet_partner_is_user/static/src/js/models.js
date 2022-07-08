// SPDX-FileCopyrightText: 2022 Coop IT Easy SC
//
// SPDX-License-Identifier: AGPL-3.0-or-later
odoo.define("pos_customer_wallet_partner_is_user.models", function (require) {
    "use strict";

    var models = require("point_of_sale.models");

    models.load_fields("res.partner", ["is_customer_wallet_user"]);

    var order_prototype = models.Order.prototype;
    models.Order = models.Order.extend({
        export_for_printing: function () {
            var receipt = order_prototype.export_for_printing.apply(this);
            var client = this.get("client");
            receipt.is_customer_wallet_user = client
                ? client.is_customer_wallet_user
                : null;
            return receipt;
        },
    });
});
