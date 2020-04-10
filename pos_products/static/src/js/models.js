odoo.define('pos_products.models', function (require) {
    "use strict";

    var models = require('point_of_sale.models');
    var super_posmodel = models.PosModel.prototype;

    models.PosModel = models.PosModel.extend({
        initialize: function (session, attributes) {
            // New code
            var product_product = _.find(this.models, function (model) {
                return model.model === 'product.product';
            });
            product_product.fields.push('display_weight', 'display_unit', 'main_seller_id');
            // Inheritance
            return super_posmodel.initialize.call(this, session, attributes);
        },
    });
});
