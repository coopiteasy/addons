openerp.pos_mirror = function(instance, module) {
    var _t = instance.web._t;
    var QWeb = instance.web.qweb;
    var round_di = instance.web.round_decimals;
    var round_pr = instance.web.round_precision;

    instance.point_of_sale.URLLinkPopupWidget = instance.point_of_sale.PopUpWidget
        .extend({
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
    instance.point_of_sale.OrderButtonWidget.include({
            selectOrder: function(event) {
                this._super(event);
                var self = this;
                pos = self.pos;
                selectedOrder = pos.get('selectedOrder');
                currentOrderLines = selectedOrder.get('orderLines');
                orderLines = [];
                (currentOrderLines).each(_.bind(function(item) {
                    var t = item.export_as_JSON();
                    var product = self.pos.db.get_product_by_id(
                        t.product_id);
                    pro_info = [product.display_name, t
                        .price_unit, t.qty, product
                        .uom_id[1], t.discount
                    ];
                    return orderLines.push(pro_info);
                }, this));
                orderLines.push([selectedOrder.getTax(),
                    selectedOrder.getTotalTaxIncluded()
                ]);
                customer_id = selectedOrder.get_client() &&
                    selectedOrder.get_client().id || '';
                (new instance.web.Model('mirror.image.order')).get_func
                    ('store_pos_data')(orderLines, self.pos.session
                        .session_id).pipe(
                        function(result) {
                            console.log("Call server from qty")
                        });
            },
        }),
        instance.point_of_sale.PosWidget.include({
            show: function() {
                var self = this;
                this._super();

            },
            build_widgets: function() {
                var self = this;
                this._super();
                this.url_screen = new instance.point_of_sale.URLLinkPopupWidget(
                    this, {});
                this.url_screen.appendTo(this.$el);
                this.screen_selector.popup_set['url_screen'] = this
                    .url_screen;
                this.url_screen.hide();
                this.$('.url_create').click(function() {
                    pos = self.pos;
                    selectedOrder = pos.get('selectedOrder');
                    currentOrderLines = selectedOrder.get(
                        'orderLines');
                    orderLines = [];
                    (currentOrderLines).each(_.bind(
                        function(item) {
                            var t = item.export_as_JSON();
                            var product = self.pos.db
                                .get_product_by_id(
                                    t.product_id);
                            pro_info = [product.display_name,
                                t.price_unit, t
                                .qty, product.uom_id[
                                    1], t.discount
                            ];
                            return orderLines.push(
                                pro_info);
                        }, this));
                    orderLines.push([selectedOrder.getTax(),
                        selectedOrder.getTotalTaxIncluded()
                    ]);
                    (new instance.web.Model(
                        'mirror.image.order'
                    )).get_func(
                        'create_pos_data')(
                        orderLines,
                        selectedOrder.uid,
                        self.pos.session
                        .session_id, self.pos
                        .currency.symbol,
                        self.pos.pos_session
                        .name).pipe(
                        function(result) {
                            console.log(
                                "Call server from qty"
                            )
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
                (new instance.web.Model('mirror.image.order')).get_func
                    ('delete_pos_data')(self.pos.session.session_id)
                    .pipe(
                        function(result) {
                            console.log("Call server from qty")
                        });
                this._super();
            },
            delete_mirror_data: function() {
                var self = this;
                (new instance.web.Model('mirror.image.order')).get_func
                    ('delete_pos_data')()
                    .pipe(
                        function(result) {
                            console.log("Call server from qty")
                        });
            }
        });

    var _super_Order = instance.point_of_sale.Order.prototype;
    instance.point_of_sale.Order = instance.point_of_sale.Order.extend({
        addProduct: function(product, options) {
            var self = this;
            _super_Order.addProduct.call(this, product, options);
            pos = self.pos;
            selectedOrder = pos.get('selectedOrder');
            currentOrderLines = selectedOrder.get('orderLines');
            orderLines = [];
            (currentOrderLines).each(_.bind(function(item) {
                var t = item.export_as_JSON();
                var product = self.pos.db.get_product_by_id(
                    t.product_id);
                pro_info = [product.display_name, t
                    .price_unit, t.qty, product
                    .uom_id[1], t.discount
                ];
                return orderLines.push(pro_info);
            }, this));
            orderLines.push([selectedOrder.getTax(),
                selectedOrder.getTotalTaxIncluded()
            ]);
            customer_id = selectedOrder.get_client() &&
                selectedOrder.get_client().id || '';
            (new instance.web.Model('mirror.image.order')).get_func
                ('store_pos_data')(orderLines, self.pos.session
                    .session_id).pipe(
                    function(result) {
                        console.log("Call server from qty")
                    });
        },
    });

    instance.point_of_sale.NumpadWidget.include({
        start: function() {
            var self = this;
            this._super();
            this.$(".input-button").click(function() {
                pos = self.pos;
                selectedOrder = pos.get('selectedOrder');
                currentOrderLines = selectedOrder.get(
                    'orderLines');
                orderLines = [];
                (currentOrderLines).each(_.bind(
                    function(item) {
                        var t = item.export_as_JSON();
                        var product = self.pos.db
                            .get_product_by_id(
                                t.product_id);
                        pro_info = [product.display_name,
                            t.price_unit, t
                            .qty, product.uom_id[
                                1], t.discount
                        ];
                        return orderLines.push(
                            pro_info);
                    }, this));
                orderLines.push([selectedOrder.getTax(),
                    selectedOrder.getTotalTaxIncluded()
                ]);
                customer_id = selectedOrder.get_client() &&
                    selectedOrder.get_client().id || '';
                (new instance.web.Model(
                    'mirror.image.order')).get_func(
                    'store_pos_data')(orderLines,
                    self.pos.session.session_id).pipe(
                    function(result) {
                        console.log(
                            "Call server from qty"
                        )
                    });
            });
        },
    });
    instance.point_of_sale.ReceiptScreenWidget.include({
        template: 'ReceiptScreenWidget',
        finishOrder: function() {
            this.pos.get('selectedOrder').destroy();
            var self = this;
            pos = self.pos;
            selectedOrder = pos.get('selectedOrder');
            customer_id = selectedOrder.get_client() &&
                selectedOrder.get_client().id || '';
            (new instance.web.Model('mirror.image.order')).get_func
                ('store_pos_data')([], self.pos.session.session_id)
                .pipe(
                    function(result) {
                        console.log("Call server from qty")
                    });
        },

    });
}
