odoo.define("auth_company_signup.auth_signup", function (require) {
    "use strict";

    $(document).ready(function () {
        $("input[name='is_company']").click(function (ev) {
            var val = $("input[name='is_company']:checked").val();
            if (val == "on") {
                $("div[name='vat_div']").show("quick");
            } else {
                $("div[name='vat_div']").hide("quick");
            }
        });
    });
});
