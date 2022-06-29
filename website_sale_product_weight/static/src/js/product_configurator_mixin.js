// SPDX-FileCopyrightText: 2022 Coop IT Easy SC
//
// SPDX-License-Identifier: AGPL-3.0-or-later

odoo.define(
    "website_sale_product_weight.product_configurator_mixin",
    function (require) {
        "use strict";

        var ProductConfiguratorMixin = require("sale.ProductConfiguratorMixin");
        var animation = require("website.content.snippets.animation");

        ProductConfiguratorMixin._onChangeCombinationWeight = function (
            _ev,
            $parent,
            combination
        ) {
            var $weight = $parent.find(
                ".oe_product_weight:first .oe_product_weight_value"
            );
            $weight.html(combination.weight);

            var $weight_uom_name = $parent.find(
                ".oe_product_weight:first .oe_product_weight_uom_name_value"
            );
            $weight_uom_name.html(combination.weight_uom_name);
        };

        animation.registry.WebsiteSale.include({
            _onChangeCombination: function () {
                this._super.apply(this, arguments);
                ProductConfiguratorMixin._onChangeCombinationWeight.apply(
                    this,
                    arguments
                );
            },
        });

        return ProductConfiguratorMixin;
    }
);
