odoo.define("pos_solidarity_rounding.screens", function (require) {
    "use strict";

    var screens = require("point_of_sale.screens");

    screens.ClientListScreenWidget.include({
        // This function normally resets the pricelist, also resetting the
        // prices of all products. We want to preserve the tip amount when
        // changing the selected client.
        save_changes: function () {
            var order = this.pos.get_order();
            var tip = order.get_tip();
            this._super();
            if (tip) {
                order.set_tip(tip);
            }
        },
    });
});
