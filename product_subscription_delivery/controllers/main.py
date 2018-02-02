# -*- coding: utf-8 -*-

from openerp.http import request
from openerp.addons.website_product_subscription.controllers.main import WebsiteProductSubscription

class WebsiteProductSubscription(WebsiteProductSubscription):
    
    def get_countries(self):
        countries = super(WebsiteProductSubscription,self).get_countries()
        shipping_countries = request.env['delivery.carrier']._get_shipping_country(countries)
        return shipping_countries
