odoo.define("pos_solidarity_rounding.models", function (require) {
    "use strict";

    var models = require("point_of_sale.models");

    models.load_fields("res.partner", ["enable_solidarity_rounding"]);

    models.Order = models.Order.extend({
        determine_tip: function () {
            var amount = this.get_total_with_tax();
            var target_amount = Math.ceil(amount);
            return target_amount - amount;
        },
    });
    return models;
});
