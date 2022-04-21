odoo.define("pos_customer_wallet.screens", function (require) {
    "use strict";
    var screens = require("point_of_sale.screens");

    screens.PaymentScreenWidget.include({
        customer_changed: function () {
            var self = this;
            var client = this.pos.get_client();

            if (client) {
                this.pos.load_partners_by_ids([client.id]).then(function () {
                    // partners may have changed in the backend
                    self.partner_cache = new screens.DomCache();

                    self.render_list(self.pos.db.get_partners_sorted(1000));

                    self.pos
                        .get_order()
                        .set_client(self.pos.get_partner_by_id(client.id));
                });
            }

            this._super();
        },
    });
});
