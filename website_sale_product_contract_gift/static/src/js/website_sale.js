odoo.define("website_sale_product_contract_gift.website_sale", function (require) {
    "use strict";

    var publicWidget = require("web.public.widget");

    publicWidget.registry.websiteSaleCartGift = publicWidget.Widget.extend({
        selector: ".oe_website_sale .oe_cart",
        events: {
            "click #gift_form_confirm_button": "_onClickConfirm",
        },

        // --------------------------------------------------------------------------
        // Handlers
        // --------------------------------------------------------------------------

        /**
         * @private
         * @param {Event} ev
         */
        _onClickConfirm: function () {
            var $form = $("form[name='gift_date']");
            $form.submit();
        },
    });

    return {
        websiteSaleCartGift: publicWidget.registry.websiteSaleCart,
    };
});
