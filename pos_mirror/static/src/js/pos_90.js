odoo.define('pos_mirror.pos_90.js', function (require) {
"use strict";

var core = require('web.core');
var gui = require('point_of_sale.gui');
var PosBaseWidget = require('point_of_sale.BaseWidget');
var Chrome = require('point_of_sale.chrome');
var Model = require('web.DataModel');
var models = require('point_of_sale.models');
var screens = require('point_of_sale.screens');
var NumberPadWidget = screens.NumpadWidget;

var _t = core._t;
var QWeb = core.qweb;

var URLLinkPopupWidget = PosBaseWidget.extend({
        template: 'URLLinkPopupWidget',
        show: function(options) {
            options = options || {};
            var self = this;
            this._super();
            this.message = options.message;
            this.renderElement();
            this.$(".press_ok").click(function() {
                self.pos_widget.screen_selector.set_current_screen(
                    'products');
            });
        },
    });

gui.define_popup({name:'alert', widget: URLLinkPopupWidget});

Chrome.Chrome.include({
    show: function() {
        var self = this;
        this._super();
    },
    build_widgets: function() {
        var self = this;
        this._super();
        this.url_screen = new URLLinkPopupWidget({pos: this.pos, chrome: this});
        this.url_screen.replace(this.url_screen.$el, this.$el);
        gui.define_popup({name:'alert', widget: this.url_screen});
        this.$('.url_create').click(function() {
            var pos = self.pos;
            var selectedOrder = pos.get('selectedOrder');
            var currentOrderLines = selectedOrder.orderlines;
            var orderLines = [];
            console.log(currentOrderLines);

            (currentOrderLines).each(_.bind(
                function(item) {
                    var t = item.export_as_JSON();
                    var product = self.pos.db
                        .get_product_by_id(
                            t.product_id);
                    var pro_info = [product.display_name,
                        t.price_unit, t
                        .qty, product.uom_id[
                            1], t.discount
                    ];
                    return orderLines.push(
                        pro_info);
                }, this));
            orderLines.push([selectedOrder.get_total_with_tax(),
                selectedOrder.get_total_tax()
            ]);
            console.log("DDD", pos)
            new Model('mirror.image.order').call('create_pos_data',[orderLines,
                selectedOrder.uid, pos.pos_session.id,
                pos.currency.symbol, pos.pos_session.name]).then(function(result){
                    console.log("Call server from qty");
                });
            var url = window.location.origin +
                "/pos/mirror?pos_session=" +
                self.pos
                .pos_session.name;

            var width = screen.width;
            var left = screen.width;

            left += screen.width;
            window.open(url, 'mirror',
                'resizable=1,scrollbars=1,fullscreen=0,height=' +
                screen.height + ',width=' +
                screen.width + ', left=' + left +
                ', toolbar=0, menubar=0,status=1'
            );
        });

     
    },

    close: function() {
        var self = this;
        new Model('mirror.image.order').call('delete_pos_data', [self.pos.pos_session.id]).then(function(result) {
                console.log("Call server from qty");
            });
        this._super();
    },
    
    delete_mirror_data: function() {
        var self = this;
        new Model('mirror.image.order').call('delete_pos_data').then(function(result) {
            console.log("Call server from qty");
        });
    }


    });

    var _super_order = models.Order.prototype;
    models.Order = models.Order.extend({
        add_product: function(product, options){
            console.log("aaaaaasdhjshadjhsjsd=============", $(this));
            var pos = this.pos;
            _super_order.add_product.apply(this,arguments);
            console.log("ssssssss", pos);
            var selectedOrder = pos.get('selectedOrder');
            var currentOrderLines = selectedOrder.orderlines;
            var orderLines = [];
            (currentOrderLines).each(_.bind(function(item) {
                var t = item.export_as_JSON();
                var product = pos.db.get_product_by_id(t.product_id);
                var pro_info = [product.display_name, t.price_unit, t.qty, 
                product.uom_id[1], t.discount];
                return orderLines.push(pro_info);
            }, this));
            orderLines.push([selectedOrder.get_total_with_tax(),
                selectedOrder.get_total_tax()
            ]);
            var customer_id = selectedOrder.get_client() &&
                selectedOrder.get_client().id || '';
            (new Model('mirror.image.order')).call('store_pos_data', [orderLines, this.pos.pos_session.id])
            .then(function(result) {
                console.log("Call server from Product")
            });
        },
    });

    NumberPadWidget.include({
            start: function(){
            var pos = this.pos;
            this._super();
             this.$(".input-button").click(function() {
                // pos = self.pos;
                 var selectedOrder = pos.get('selectedOrder');
                 var currentOrderLines = selectedOrder.orderlines
                 var orderLines = [];
                 console.log("sddddddddddsss", $(currentOrderLines));
                 (currentOrderLines).each(_.bind(
                     function(item) {
                         var t = item.export_as_JSON();
                         var product = pos.db
                             .get_product_by_id(
                                 t.product_id);
                         var pro_info = [product.display_name,
                             t.price_unit, t
                             .qty, product.uom_id[
                                 1], t.discount
                         ];
                         return orderLines.push(
                             pro_info);
                     }, this));
                 orderLines.push([selectedOrder.get_total_with_tax(),
                     selectedOrder.get_total_tax()
                 ]);
                 var customer_id = selectedOrder.get_client() &&
                     selectedOrder.get_client().id || '';
                 (new Model('mirror.image.order')).call('store_pos_data', [orderLines, pos.pos_session.id])
                    .then(function(result) {
                        console.log("Call server from Product");
                    });
                });
        },
    });
    Chrome.OrderSelectorWidget.include({
        order_click_handler: function(event, $el) {
                 this._super(event, $el);
                var pos = this.pos;
                var selectedOrder = pos.get('selectedOrder');
                var currentOrderLines = selectedOrder.orderlines;
                var orderLines = [];
                (currentOrderLines).each(_.bind(function(item) {
                    var t = item.export_as_JSON();
                    var product = pos.db.get_product_by_id(
                        t.product_id);
                    var pro_info = [product.display_name, t
                        .price_unit, t.qty, product
                        .uom_id[1], t.discount
                    ];
                    return orderLines.push(pro_info);
                }, this));
                orderLines.push([selectedOrder.get_total_with_tax(),
                    selectedOrder.get_total_tax()
                ]);
                var customer_id = selectedOrder.get_client() &&
                    selectedOrder.get_client().id || '';
                (new Model('mirror.image.order')).call('store_pos_data', [orderLines, this.pos.pos_session.id])
                .then(function(result) {
                    console.log("Call server from Product")
                });
             },

      neworder_click_handler:function(event, $el){
         this._super(event, $el);
                var pos = this.pos;
                var selectedOrder = pos.get('selectedOrder');
                var currentOrderLines = selectedOrder.orderlines;
                var orderLines = [];
                (currentOrderLines).each(_.bind(function(item) {
                    var t = item.export_as_JSON();
                    var product = pos.db.get_product_by_id(
                        t.product_id);
                    var pro_info = [product.display_name, t
                        .price_unit, t.qty, product
                        .uom_id[1], t.discount
                    ];
                    return orderLines.push(pro_info);
                }, this));
                orderLines.push([selectedOrder.get_total_with_tax(),
                    selectedOrder.get_total_tax()
                ]);
                var customer_id = selectedOrder.get_client() &&
                    selectedOrder.get_client().id || '';
                (new Model('mirror.image.order')).call('store_pos_data', [orderLines, this.pos.pos_session.id])
                .then(function(result) {
                    console.log("Call server from Product")
                });
         },
    deleteorder_click_handler: function(event, $el) {
        this._super(event, $el);
        var pos = this.pos;
                var selectedOrder = pos.get('selectedOrder');
                var currentOrderLines = selectedOrder.orderlines;
                var orderLines = [];
                (currentOrderLines).each(_.bind(function(item) {
                    var t = item.export_as_JSON();
                    var product = pos.db.get_product_by_id(
                        t.product_id);
                    var pro_info = [product.display_name, t
                        .price_unit, t.qty, product
                        .uom_id[1], t.discount
                    ];
                    return orderLines.push(pro_info);
                }, this));
                orderLines.push([selectedOrder.get_total_with_tax(),
                    selectedOrder.get_total_tax()
                ]);
                var customer_id = selectedOrder.get_client() &&
                    selectedOrder.get_client().id || '';
                (new Model('mirror.image.order')).call('store_pos_data', [orderLines, this.pos.pos_session.id])
                .then(function(result) {
                    console.log("Call server from Product")
                });
    },
    });

    screens.ReceiptScreenWidget.include({
        click_next: function() {
            this.pos.get('selectedOrder').destroy();
            this._super();
            var pos = this.pos;
                var selectedOrder = pos.get('selectedOrder');
                var currentOrderLines = selectedOrder.orderlines;
                var orderLines = [];
                (currentOrderLines).each(_.bind(function(item) {
                    var t = item.export_as_JSON();
                    var product = pos.db.get_product_by_id(
                        t.product_id);
                    var pro_info = [product.display_name, t
                        .price_unit, t.qty, product
                        .uom_id[1], t.discount
                    ];
                    return orderLines.push(pro_info);
                }, this));
                orderLines.push([selectedOrder.get_total_with_tax(),
                    selectedOrder.get_total_tax()
                ]);
                var customer_id = selectedOrder.get_client() &&
                    selectedOrder.get_client().id || '';
                (new Model('mirror.image.order')).call('store_pos_data', [orderLines, this.pos.pos_session.id])
                .then(function(result) {
                    console.log("Call server from Product")
                });
        },
    });
});




