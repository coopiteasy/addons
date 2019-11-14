/*
    POS Search with Accented/Unaccented characters module for Odoo
    Copyright (C) 2019 Coop IT Easy
    @author: Vincent Van Rossem <vincent@coopiteasy.be>
    The licence is in the file __openerp__.py
*/
odoo.define('pos_search_accented_unaccented', function (require) {
    "use strict";

    var PosDB = require('point_of_sale.DB');

    PosDB.include({

        _product_search_string: function (product) {
            var str = product.display_name;

            // surchage starts here
            str += '|' + product.display_name.normalize("NFD").replace(/[\u0300-\u036f]/g, "");
            // surcharge ends here

            if (product.barcode) {
                str += '|' + product.barcode;
            }
            if (product.default_code) {
                str += '|' + product.default_code;
            }
            if (product.description) {
                str += '|' + product.description;
            }
            if (product.description_sale) {
                str += '|' + product.description_sale;
            }
            var packagings = this.packagings_by_product_tmpl_id[product.product_tmpl_id] || [];
            for (var i = 0; i < packagings.length; i++) {
                str += '|' + packagings[i].barcode;
            }
            str = product.id + ':' + str.replace(/:/g, '') + '\n';
            return str;
        },
    })
});
