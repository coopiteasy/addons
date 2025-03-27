/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

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
     */
    _onClickConfirm: function () {
        var $form = $("form[name='gift_date']");
        $form.submit();
    },
});

export default publicWidget.registry.websiteSaleCartGift;
