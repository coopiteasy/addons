# -*- coding: utf-8 -*-
from openerp import http
from openerp.http import request
from openerp.tools.translate import _

from openerp.exceptions import ValidationError


class WebsiteProductSubscription(http.Controller):

    @http.route(['/page/login_subscriber',
                 '/login_subscriber'],
                type='http',
                auth="user",
                website=True)
    def login_subscriber(self, **kwargs):

        return request.redirect("/page/become_subscriber")

    @http.route(['/page/become_subscriber',
                 '/become_subscriber'],
                type='http',
                auth="public",
                website=True)
    def display_subscription_page(self, **kwargs):
        values = {}

        values = self.fill_values(values, True)

        for field in ['email', 'firstname', 'lastname', 'address', 'city',
                      'zip_code', 'country_id', 'error_msg']:
            if kwargs.get(field):
                values[field] = kwargs.pop(field)

        values.update(kwargs=kwargs.items())
        return request.website.render("website_product_subscription.becomesubscriber", values)

    def fill_values(self, values, load_from_user=False):
        sub_temp_obj = request.env['product.subscription.template']
        if load_from_user:
            # the subscriber is connected
            if request.env.user.login != 'public':
                values['logged'] = 'on'
                partner = request.env.user.partner_id
                values['firstname'] = partner.firstname
                values['lastname'] = partner.lastname
                values['email'] = partner.email
                values['street'] = partner.street
                values['zip_code'] = partner.zip
                values['city'] = partner.city
                values['country_id'] = partner.country_id.id
                if partner.parent_id:
                    values['company'] = partner.parent_id.display_name

        if not values.get('product_subscription_id', False):
            values['product_subscription_id'] = 0
        values['subscriptions'] = sub_temp_obj.sudo().search([('publish', '=', True)])
        values['countries'] = self.get_countries()

        if not values.get('country_id'):
            values['country_id'] = '21'
        return values

    def get_countries(self):
        countries = request.env['res.country'].sudo().search([])

        return countries

    def get_address(self, kwargs):
        vals = {'zip': kwargs.get("zip_code"),
                'city': kwargs.get("city"),
                'country_id': kwargs.get("country_id")}
        address = kwargs.get("street") + ', ' + kwargs.get("street_number")
        if kwargs.get("box").strip() != '':
            address = address + ', ' + kwargs.get("box").strip()
        vals['street'] = address
        return vals

    def get_receiver(self, kwargs):
        vals = {'email': kwargs.get("subscriber_email"),
                'out_inv_comm_type': 'bba',
                'out_inv_comm_algorithm': 'random'}
        firstname = kwargs.get("subscriber_firstname").title()
        lastname = kwargs.get("subscriber_lastname").upper()
        vals['name'] = firstname + ' ' + lastname
        vals['firstname'] = firstname
        vals['lastname'] = lastname
        vals["customer"] = True

        return vals

    @http.route(['/product_subscription/subscribe'], type='http', auth="public", website=True)
    def product_subscription(self, **kwargs):
        partner_obj = request.env['res.partner']
        user_obj = request.env['res.users']
        values = {}
        redirect = "website_product_subscription.becomesubscriber"

        if 'g-recaptcha-response' not in kwargs or not request.website.is_captcha_valid(kwargs['g-recaptcha-response']):
            values = self.fill_values(values)
            values.update(kwargs)
            values["error_msg"] = _("the captcha has not been validated, "
                                    "please fill in the captcha")

            return request.website.render(redirect, values)

        logged = kwargs.get("logged") == 'on'
        gift = kwargs.get("gift") == 'on'

        if not logged and kwargs.get("email") != kwargs.get("email_confirmation"):
            values = self.fill_values(values)
            values.update(kwargs)
            values["error_msg"] = "email and confirmation email doesn't match"
            return request.website.render(redirect, values)

        if not logged and 'email' in kwargs:
            user = user_obj.sudo().search([('login', '=', kwargs.get("email"))])
            if user:
                values = self.fill_values(values)
                values.update(kwargs)
                values["error_msg"] = _("There is an existing account for "
                                        "this mail address. Please login "
                                        "before fill in the form")

                return request.website.render(redirect, values)

        if gift:
            values["gift"] = gift

        subscriber = False
        sponsor = False
        subscriber_vals = {}
        if logged:
            subscriber = request.env.user.partner_id
            address = self.get_address(kwargs)
            if gift:
                sponsor = request.env.user.partner_id
                subscriber_vals.update(self.get_receiver(kwargs))
                subscriber_vals.update(address)
                subscriber = partner_obj.sudo().create(subscriber_vals)
            else:
                subscriber.sudo().write(address)
        else:
            lastname = kwargs.get("lastname").upper()
            firstname = kwargs.get("firstname").title()

            subscriber_vals["name"] = firstname + " " + lastname
            subscriber_vals["lastname"] = lastname
            subscriber_vals["firstname"] = firstname
            subscriber_vals["email"] = kwargs.get("email")
            subscriber_vals["out_inv_comm_type"] = 'bba'
            subscriber_vals["out_inv_comm_algorithm"] = 'random'
            subscriber_vals["customer"] = True

            if gift:
                receiver_vals = self.get_receiver(kwargs)
                receiver_vals.update(self.get_address(kwargs))
                subscriber = partner_obj.sudo().create(receiver_vals)
                sponsor = partner_obj.sudo().create(subscriber_vals)
            else:
                subscriber_vals.update(self.get_address(kwargs))
                subscriber = partner_obj.sudo().create(subscriber_vals)

        values['subscriber'] = subscriber.id
        user_values = {'partner_id': subscriber.id, 'login': subscriber.email}
        if sponsor:
            values['sponsor'] = sponsor.id
            user_values['partner_id'] = sponsor.id
            user_values['login'] = sponsor.email

        values["subscription_template"] = int(kwargs.get("product_subscription_id"))

        request.env['product.subscription.request'].sudo().create(values)

        if not logged:
            if "company" in kwargs and kwargs.get("company").strip() != '':

                vat_number = ''
                if "vat_number" in kwargs and kwargs.get("vat_number").strip() != '':
                    vat_number = kwargs.get("vat_number").strip()

                company_vals = {
                    'name': kwargs.get("company"),
                    'email': subscriber.email,
                    'out_inv_comm_type': 'bba',
                    'out_inv_comm_algorithm': 'random',
                    'vat': vat_number,
                }
                try:

                    company = partner_obj.sudo().create(company_vals)
                except ValidationError as ve:
                    values = self.fill_values(values)
                    values.update(kwargs)
                    values['error_msg'] = ve.name
                    return request.website.render(redirect, values)

                # create user last to avoid creating a user when
                # an error occurs
                user_id = user_obj.sudo()._signup_create_user(user_values)
                user = user_obj.browse(user_id)
                user.sudo().with_context({'create_user': True}).action_reset_password()

                subscriber.sudo().write({'parent_id': company.id})
        return request.website.render('website_product_subscription.product_subscription_thanks',values)
