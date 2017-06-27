

$(document).ready(function (require) {

odoo.define('website_sale.cart', function (require) {
"use strict";
var ajax = require('web.ajax');
$('.oe_website_sale').each(function () {
    var $oe_website_sale = this;
 	
   $($oe_website_sale).on("change", ".oe_cart1 input.js_quantity", function (ev) {
        ev.preventDefault();
        var $input = $(this);
        var value = parseInt($input.val(), 10);
        var line_id = parseInt($input.data('line-id'),10);
        var product_id = parseInt($input.data('product-id'),10);
        if (isNaN(value)) value = 0;
        ajax.jsonRpc("/shop/cart/update_json", 'call', {
            'line_id': line_id,
            'product_id': parseInt($input.data('product-id'),10),
            'set_qty': value})
            .then(function (data) {
                if (!data.quantity) {
                    window.location.href = document.URL;
                    return false;
                }
                var $q = $(".my_cart_quantity");
                $q.parent().parent().removeClass("hidden", !data.quantity);
                $q.html(data.cart_quantity).hide().fadeIn(600);

                $input.val(data.quantity);
                $('input[name="'+product_id+'"]').val(data.quantity);
                $('.js_quantity[data-line-id='+line_id+']').val(data.quantity).html(data.quantity);
                $("#cart_total").replaceWith(data['website_sale.total']);
                return false;
            });
            return false;
    });

    $($oe_website_sale).on("change", ".oe_product input.js_quantity_inherited", function () {
        var $input = $(this);
        var value = parseInt($input.val(), 10);
        if (isNaN(value)) value = 0;
        ajax.jsonRpc("/shop/cart/update_json_shop_to_qty", 'call', {
        'product_id': parseInt($input.attr('name'),10),
        'set_qty': value})
        .then(function (data) {
        if (!data.quantity) {
            location.reload();
            return;
        }
        var $q = $(".my_cart_quantity");
        $q.parent().parent().removeClass("hidden", !data.quantity);
        $q.html(data.cart_quantity).hide().fadeIn(600);
		var $p_id = parseInt($input.attr('name'),10);
        $('input[data-product-id="'+$p_id+'"]').val(data.quantity);
		$("#div_cart_total_new").replaceWith(data['website_sale.total']);
        $input.val(data.quantity);
        $("#cart_total").replaceWith(data['website_sale.total']);
        return;
        });
    });




    $($oe_website_sale).on("change", "input.js_quantity_inherited2", function (ev) {
        ev.preventDefault();
        var $input = $(this);
        var value = parseInt($input.val(), 10);
        var product_id = $('#int_current_prod_variant_id').val(); 
        if (isNaN(value)) value = 0;
        ajax.jsonRpc("/shop/cart/update_json_shop_to_qty", 'call', {
        'product_id': product_id,//$('#int_current_prod_variant_id'),
        'set_qty': value})
        .then(function (data) {
        if (!data.quantity) {
            location.reload();
            return;
        }
        var $q = $(".my_cart_quantity");
        $q.parent().parent().removeClass("hidden", !data.quantity);
        $q.html(data.cart_quantity).hide().fadeIn(600);

		var $p_id = parseInt($input.attr('name'),10);
        $('input[data-product-id="'+$p_id+'"]').val(data.quantity);
		$("#div_cart_total_new").replaceWith(data['website_sale.total']);
        $input.val(data.quantity);
		console.log(data.quantity+ ' my quantity ');
        $("#cart_total").replaceWith(data['website_sale.total']);
        return;
        });

    });

 // inheriting original to set max to 99
 // hack to add and remove from cart with json
    var $my_qty_max = 99;
    $($oe_website_sale).on('click', 'a.js_add_cart_json_inherited', function (ev) {
        ev.preventDefault();
        var $link = $(ev.currentTarget);
        var $input = $link.parent().parent().find("input");
        var min = parseFloat($input.data("min") || 0);
        var max = parseFloat($input.data("max") || $my_qty_max); //Infinity);
		var $p_id = parseInt($input.data('product-id'),10);
        var quantity = ($link.has(".fa-minus").length ? -1 : 1) + parseFloat($input.val(),10);
        $input.val(quantity > min ? (quantity < max ? quantity : max) : min);
		$('input[name="'+$p_id+'"]').val(quantity > min ? (quantity < max ? quantity : max) : min);
		$input.change();
        return false;
    });


	$($oe_website_sale).on("change", ".oe_cart input.js_quantity", function (ev) {
        ev.preventDefault();
        var $input = $(this);
        var value = parseInt($input.val(), 10);
        var line_id = parseInt($input.data('line-id'),10);
        if (isNaN(value)) value = 0;
        ajax.jsonRpc("/shop/cart/update_json", 'call', {
            'line_id': line_id,
            'product_id': parseInt($input.data('product-id'),10),
            'set_qty': value})
            .then(function (data) {
                if (!data.quantity) {
                    window.location.href = document.URL;
                    return false;
                }
                var $q = $(".my_cart_quantity");
                $q.parent().parent().removeClass("hidden", !data.quantity);
                $q.html(data.cart_quantity).hide().fadeIn(600);

                $input.val(data.quantity);
                $('.js_quantity[data-line-id='+line_id+']').val(data.quantity).html(data.quantity);
                $("#cart_total").replaceWith(data['website_sale.total']);
                return false;
            });
            return false;
    });



 // inheriting original to set max to 99
 // hack to add and remove from cart with json
    var $my_qty_max = 99;
    $($oe_website_sale).on('click', 'a.js_add_cart_json_inherited2', function (ev) {
    	ev.stopImmediatePropagation();
        ev.preventDefault();
        var $link = $(ev.currentTarget);
        var $input = $link.parent().parent().find("input");
        var min = parseFloat($input.data("min") || 0);
        var max = parseFloat($input.data("max") || $my_qty_max); //Infinity);
        //var $p_id = parseInt($input.data('product-id'),10);
        var $p_id = document.getElementsByName("product_id")[0].value;
        var quantity = ($link.has(".fa-minus").length ? -1 : 1) + parseFloat($input.val(),10);
        $input.val(quantity > min ? (quantity < max ? quantity : max) : min);
        $('input[name="'+$p_id+'"]').val(quantity > min ? (quantity < max ? quantity : max) : min);
        $input.change();
        return false;
    });

 	$($oe_website_sale).on("change", ".oe_cart1 input.js_quantity", function (ev) {
        ev.preventDefault();
        var $input = $(this);
        var value = parseInt($input.val(), 10);
        var line_id = parseInt($input.data('line-id'),10);
        if (isNaN(value)) value = 0;
        ajax.jsonRpc("/shop/cart/update_json", 'call', {
            'line_id': line_id,
            'product_id': parseInt($input.data('product-id'),10),
            'set_qty': value})
            .then(function (data) {
                if (!data.quantity) {
                    window.location.href = document.URL;
                    return false;
                }
                /* TO RELOAD/REPLACE TOTAL VIEW OF CART*/
                $("#div_cart_total_new").replaceWith(data['website_sale.total']);

                var $q = $(".my_cart_quantity");
                $q.parent().parent().removeClass("hidden", !data.quantity);
                $q.html(data.cart_quantity).hide().fadeIn(600);
                $input.val(data.quantity);
                $('.js_quantity[data-line-id='+line_id+']').val(data.quantity).html(data.quantity);
                $("#cart_total").replaceWith(data['website_sale.total']);
                return false;
            });
    	});
        return false;

});
});
function on_load_call()
{
     var url = window.location.href;
     if(url.indexOf('/shop/product/') != -1){
        // called function does nothing
    	//result = hide_all_add_to_cart_elements();
        var product_id = document.getElementsByName("product_id")[0].value;
        $("#int_current_prod_variant_id").val(product_id);
        result = get_cart_qty_for_selected_variant(product_id);
   }
}
on_load_call();

});


function allow_numeric_input(e) {
 	// Allow: backspace, delete, tab, escape and enter (REMOVED: . == 190, decimalpoint == 110 )
	if ($.inArray(e.keyCode, [46, 8, 9, 27, 13]) !== -1 ||
	    // Allow: Ctrl+A, Command+A
	    (e.keyCode == 65 && ( e.ctrlKey === true || e.metaKey === true ) ) || 
	    // Allow: home, end, left, right, down, up
	    (e.keyCode >= 35 && e.keyCode <= 40)) {
		 // let it happen, don't do anything
		 return;
	}
        // Allow: 9+0=90, avoid: 0+9=09.
        var qty_inputed_value = document.getElementById("cart_quantity_txt_box").value;
        if (e.keyCode == 48 && qty_inputed_value < 1) {
            e.preventDefault();
        }
	if ((e.shiftKey || (e.keyCode < 48 || e.keyCode > 57)) && (e.keyCode < 96 || e.keyCode > 105)) {
	    e.preventDefault();
	}
}



