odoo.define("pos_solidarity_rounding.screens", function (require) {
    "use strict";

    var screens = require("point_of_sale.screens");

    // screens.ActionpadWidget.include({
    //     renderElement: function() {
    //         var self = this;
    //         this._super();
    //         this.$('.pay').click(function(){
    //             var order = self.pos.get_order();
    //             // Don't tip on top of tips; set tip to 0 first.
    //             order.set_tip(0);
    //             var tip = order.determine_tip();
    //             order.set_tip(tip);
    //         });
    //     },
    // });
});
