odoo.define("pos_customer_wallet.screens", function (require) {
    "use strict";
    var models = require("point_of_sale.models");
    var rpc = require("web.rpc");

    models.PosModel = models.PosModel.extend({
        // Code largely borrowed from point_of_sale.load_new_partners.
        load_partners_by_ids: function (ids) {
            var self = this;
            var def = new $.Deferred();
            var fields = _.find(this.models, function (model) {
                return model.model === "res.partner";
            }).fields;

            rpc.query(
                {
                    model: "res.partner",
                    method: "read",
                    args: [ids, fields],
                },
                {
                    timeout: 3000,
                    shadow: true,
                }
            ).then(
                function (partners) {
                    if (self.db.add_partners(partners)) {
                        // check if the partners we got were real updates
                        def.resolve();
                    } else {
                        def.reject();
                    }
                },
                function (type, err) {
                    def.reject();
                }
            );
            return def;
        },
    });
});
