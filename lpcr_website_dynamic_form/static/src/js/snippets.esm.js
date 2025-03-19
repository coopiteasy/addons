/** @odoo-module **/

import "website.s_website_form";
import {patch} from "@web/core/utils/patch";
import publicWidget from "web.public.widget";

patch(publicWidget.registry.s_website_form.prototype, "lpcr_website dynamic_form", {
    async send() {
        console.log("coucou");
        return this._super(...arguments);
    },
});
