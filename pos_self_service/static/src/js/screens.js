odoo.define('pos_self_service.screens', function (require) {
    "use strict";

    var PosBaseWidget = require('point_of_sale.BaseWidget');
    var chrome = require('point_of_sale.chrome');
    var gui = require('point_of_sale.gui');
    var screens = require('point_of_sale.screens');

    /*--------------------------------------*\
     |        THE SELF-SERVICE SCREEN       |
    \*======================================*/

    // The Self-Service Screen is composed of :
    // - a leftpane, containing the SelfServiceScaleWidget
    // - a rightpane, containing the SelfServiceLabelWidget

    /* --------- The Self-Service Scale --------- */

    var SelfServiceScaleWidget = PosBaseWidget.extend({
        template: 'SelfServiceScaleWidget',

        init: function(parent, options) {
            console.log("[SelfServiceScaleWidget] init")
            this._super(parent,options);
            this.weight = 0;
        },
        start: function(){
            console.log("[SelfServiceScaleWidget] start")
            var self = this;
            this._super();
            var queue = this.pos.proxy_queue;

            this.set_weight(0);
            this.renderElement();

            queue.schedule(function(){
                return self.pos.proxy.scale_read().then(function(scale_answer){
                    self.set_weight(scale_answer.weight);
                });
            },{duration:500, repeat: true});
        },
        set_weight: function(weight){
            this.weight = weight;
            this.$('.weight').text(this.get_weight_string());
        },
        get_weight: function(){
            return this.weight;
        },
        get_weight_string: function() {
            var defaultstr = (this.weight || 0).toFixed(3) + ' Kg';
            // TODO uom
            return defaultstr;
        },
    });

    /* ------ The Self-Service Label ------- */
    // The Self-Service Label contains :
    // - a barcode label ?
    // - a button to print the barcode label

    var SelfServiceLabelWidget = PosBaseWidget.extend({
        template: 'SelfServiceLabelWidget',

        init: function(parent, options) {
            console.log("[SelfServiceLabelWidget] init")
            this._super(parent,options);
            this.self_service_scale_widget = options.self_service_scale_widget || null;
            this.barcode_parser = this.pos.barcode_reader.barcode_parser;
            this.barcode = null;
        },

        start: function(){
            console.log("[SelfServiceLabelWidget] start")
            var self = this;
            this._super();
            this.renderElement();
        },

        renderElement(){
            console.log("[SelfServiceLabelWidget] renderElement")
            var self = this;
            this._super();
            this.$('.button.print').click(function(){
                self.click_print();
            });
        },

        click_print: function (){
            console.log("[SelfServiceLabelWidget] click_print");
            var weight = this.self_service_scale_widget.get_weight();
            console.log(weight)
            this.set_barcode(this.format_barcode(weight))
            console.log(this.get_barcode());
            // TODO render label ?

            // TODO print label
        },
        format_barcode: function (weight){
            console.log("[SelfServiceLabelWidget] format_barcode");
            // We use EAN13 barcode, it looks like `07 00000 12345 x`. First there
            // is the prefix, here 07, that is used to decide which type of
            // barcode we're dealing with. A weight barcode has then two groups
            // of five digits. The first group encodes the product id. Here the
            // product id is 00000. The second group encodes the weight in
            // grams. Here the weight is 12.345kg. The last digit of the barcode
            // is a checksum, here symbolized by x.
            var padding_size = 5;
            var void_product_id = '0'.repeat(padding_size);
            var weight_in_gram = weight * 1e3;

            if (weight_in_gram >= Math.pow(10, padding_size)) {
                throw new RangeError(_t("Maximum tare weight is 99.999kg"));
            }

            // Weight has to be padded with zeroes.
            var weight_with_padding = '0'.repeat(padding_size) + weight_in_gram;
            var padded_weight = weight_with_padding.substr(
                weight_with_padding.length - padding_size
            );
            // Builds the barcode using a placeholder checksum.
            var barcode = this.get_barcode_prefix()
                .concat(void_product_id, padded_weight)
                .concat(0);
            // Compute checksum
            var ean_checksum = this.barcode_parser.ean_checksum(barcode);
            // Replace checksum placeholder by the actual checksum.
            return barcode.substr(0, 12).concat(ean_checksum);
        },
        get_barcode_prefix: function () {
            var barcode_pattern = this.get_barcode_pattern();
            return barcode_pattern.substr(0, 2);
        },
       get_barcode_pattern: function () {
            var rules = this.get_nomenclature_rules();
            var rule = rules.filter(
                function (r) {
                    // We select the first (smallest sequence ID) barcode rule
                    // with the expected type.
                    return r.type === "tare";
                })[0];
            return rule.pattern;
        },
        get_nomenclature_rules: function () {
            return this.barcode_parser.nomenclature.rules;
        },
        get_barcode: function(){
            console.log("[SelfServiceLabelWidget] get_barcode");
            return this.barcode;
        },
        set_barcode: function(barcode){
            console.log("[SelfServiceLabelWidget] set_barcode");
            this.barcode = barcode;
        }
    });


    /* --------- The Self-Service Screen --------- */

    var SelfServiceScreenWidget = screens.ScreenWidget.extend({
        template: 'SelfServiceScreenWidget',

        start: function() {
            console.log("[SelfServiceScreenWidget] start")
            var self = this;
            this.self_service_scale_widget = new SelfServiceScaleWidget(this, {});
            this.self_service_scale_widget.replace(this.$('.placeholder-SelfServiceScaleWidget'));

            this.self_service_label_widget = new SelfServiceLabelWidget(this, {
                self_service_scale_widget: this.self_service_scale_widget,
            });
            this.self_service_label_widget.replace(this.$('.placeholder-SelfServiceLabelWidget'));
        },

        // Ignore products, discounts, and client barcodes
        barcode_product_action: function(code){},
        barcode_discount_action: function(code){},
        barcode_client_action: function(code){},

        show: function(){
            console.log("[SelfServiceScreenWidget] show")
            this._super();
            this.chrome.widget.order_selector.hide();
        },
    });

    // Add the self-service screen to the GUI
    gui.define_screen({
        'name': 'selfservice',
        'widget': SelfServiceScreenWidget,
        'condition': function(){
            return this.pos.config.iface_self_service;
        },
    });

    // Set the self-service screen as both the startup and default screen
    chrome.Chrome.include({
        build_widgets: function(){
            this._super();
            if (this.pos.config.iface_self_service) {
                this.gui.set_startup_screen('selfservice');
                this.gui.set_default_screen('selfservice');
            }
        },
    });

    return {
        SelfServiceScaleWidget: SelfServiceScaleWidget,
        SelfServiceLabelWidget: SelfServiceLabelWidget,
        SelfServiceScreenWidget: SelfServiceScreenWidget,
    }
});
