odoo.define("pos_solidarity_rounding.gui", function (require) {
    "use strict";

    var gui = require("point_of_sale.gui");

    gui.Gui.include({
        // Before showing the payment screen, add a rounded up tip.
        show_screen: function (screen_name, params, refresh, skip_close_popup) {
            if (screen_name === "payment") {
                var order = this.pos.get_order();
                var client = order.get_client();
                // Only do this for clients that have enabled it.
                if (client && client.enable_solidarity_rounding) {
                    // Don't tip on top of tips; set tip to 0 first.
                    order.set_tip(0);
                    var tip = order.determine_tip();
                    order.set_tip(tip);
                }
            }
            this._super(screen_name, params, refresh, skip_close_popup);
        },
    });
});
