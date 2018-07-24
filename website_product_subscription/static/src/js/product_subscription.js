odoo.define('website_product_subscription.oe_product_subscription', function (require) {
$(document).ready(function () {
	"use strict";
	var ajax = require('web.ajax');
	
    $(".oe_product_subscription").each(function () {

    	function hide_display() {
    		var gift = $("input[name='gift']:checked").val();
    		var logged = $("input[name='logged']:checked").val();
    		
    		if(gift == "on") {
    			$("div[name='subscriber_info_label']").show('quick');
    			$("div[name='delivery_label']").hide('quick');
    			$("div[name='subscriber_firstname']").show('quick');
    			$("div[name='subscriber_lastname']").show('quick');
    			$("div[name='subscriber_email']").show('quick');
    			$("input[name='subscriber_firstname']").prop('required',true);
    			$("input[name='subscriber_lastname']").prop('required',true);
    			$("input[name='subscriber_email']").prop('required',true);
    		} else {
    			$("div[name='subscriber_info_label']").hide('quick');
    			$("div[name='delivery_label']").show('quick');
    			$("div[name='subscriber_firstname']").hide('quick');
    			$("div[name='subscriber_lastname']").hide('quick');
    			$("div[name='subscriber_email']").hide('quick');
    			$("input[name='subscriber_firstname']").prop('required',false);
    			$("input[name='subscriber_lastname']").prop('required',false);
    			$("input[name='subscriber_email']").prop('required',false);
    		}
    		//alert(logged);
    		if(logged == "on" ){
    			$("div[name='email_confirmation_container']").hide('quick');
    			$("input[name='email_confirmation']").prop('required',false);
    			if(gift != 'on'){
	    			$("div[name='street_number_container']").hide('quick');
	    			$("input[name='street_number']").prop('required',false);
	    			$("div[name='box_container']").hide('quick');
	    			$("input[name='box']").prop('required',false);
    			}
    		}
    	}
    	hide_display();

    	function hide_display_company() {
    		var is_company = $("input[name='is_company']:checked").val();

    		console.log("in hide_display_company()");
    		console.log(is_company);

    		if(is_company == "on") {
    	        console.log("show company");
                $("div[name='company']").show('quick');
                $("div[name='vat_number']").show('quick');
    			$("input[name='company']").prop('required', true);
    		} else {
    	        console.log("hide company");
                $("div[name='company']").hide('quick');
                $("div[name='vat_number']").hide('quick');
    			$("input[name='company']").prop('required', false);
    		}
    	}
    	hide_display_company();

    	$("input[name='gift']").click(function(ev) {
    		hide_display();
		});
    	$("input[name='is_company']").click(function(ev) {
    		hide_display_company();
		});
    });
});
});
