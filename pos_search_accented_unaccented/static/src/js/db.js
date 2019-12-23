/*
    POS Search with Accented/Unaccented characters module for Odoo
    Copyright 2019 Coop IT Easy SCRLfs
    @author: Vincent Van Rossem <vincent@coopiteasy.be>
    License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
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
            str = product.id + ':' + str.replace(/:/g, '') + '\n';
            return str;
        },
    })
});
