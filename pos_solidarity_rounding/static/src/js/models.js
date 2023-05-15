odoo.define("pos_solidarity_rounding.models", function(require) {
    "use strict";

    var models = require("point_of_sale.models");

    models.load_fields("res.partner", ["enable_solidarity_rounding"]);

    models.Order = models.Order.extend({
        determine_tip: function() {
            var amount = this.get_total_with_tax();
            var target_amount = Math.ceil(amount);
            return target_amount - amount;
        },
        tip_exists: function() {
            var lines = this.get_orderlines();
            var tip_product = this.pos.db.get_product_by_id(
                this.pos.config.tip_product_id[0]
            );

            if (tip_product) {
                for (var i = 0; i < lines.length; i++) {
                    if (lines[i].get_product() === tip_product) {
                        return true;
                    }
                }
            }
            return false;
        },
    });
    return models;
});
