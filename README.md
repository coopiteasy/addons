
[![Pre-commit Status](https://github.com/coopiteasy/addons/actions/workflows/pre-commit.yml/badge.svg?branch=12.0)](https://github.com/coopiteasy/addons/actions/workflows/pre-commit.yml?query=branch%3A12.0)
[![Build Status](https://github.com/coopiteasy/addons/actions/workflows/test.yml/badge.svg?branch=12.0)](https://github.com/coopiteasy/addons/actions/workflows/test.yml?query=branch%3A12.0)
[![codecov](https://codecov.io/gh/coopiteasy/addons/branch/12.0/graph/badge.svg)](https://codecov.io/gh/coopiteasy/addons)

<!-- /!\ do not modify above this line -->

# IT management tools for the social economy

TODO

We are a young IT cooperative aiming at providing IT management tools and
services to social economy actors for a sustainable budget.

How ? We provide tailored-made solutions for your business using Odoo Community,
an open source management software. We offer operational support during and
after the development as well as training to allow you to manage the tools
yourself.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_customer_wallet](account_customer_wallet/) | 12.0.1.2.0 |  | Allow customers to pay using a wallet which is tracked by the company.
[account_invoice_check_bba_com](account_invoice_check_bba_com/) | 12.0.1.0.0 |  | Check the structured communication if the supplier invoice communication is of type bba.
[account_invoice_check_identical_invoice](account_invoice_check_identical_invoice/) | 12.0.1.0.0 |  | Check if invoices with the same partner, invoice date and total amount already exist
[account_invoice_correction](account_invoice_correction/) | 12.0.1.0.0 |  | Correction of taxes and account on invoice
[account_invoice_default_account_date](account_invoice_default_account_date/) | 12.0.1.0.0 |  | Sets the accounting date to the invoice date by default.
[account_invoice_line_update](account_invoice_line_update/) | 12.0.1.0.0 |  | Update invoice lines to reload the right taxes on the lines.
[account_invoice_provider_reference](account_invoice_provider_reference/) | 12.0.1.0.0 |  | Invoice Provider Reference
[account_invoice_reminder](account_invoice_reminder/) | 12.0.1.0.0 |  | This module just adds two fields to say when we sent a payment reminder to the customer and the level of the reminder.
[account_invoice_save_check_duplicate](account_invoice_save_check_duplicate/) | 12.0.1.0.0 |  | Check that account invoice hasn't been encoded twice when creating or saving. This step is normally done when validating. This step doesn't replace the validation.
[account_invoice_ubl_mass_download](account_invoice_ubl_mass_download/) | 12.0.1.0.0 |  | Account Invoice UBL Mass Download
[auth_company_signup](auth_company_signup/) | 12.0.1.0.0 |  | This module allows a user to sign up as a company.
[belgian_bank_data](belgian_bank_data/) | 12.0.1.0.0 |  | This module imports Belgian banks with their name and BIC code.
[company_today](company_today/) | 12.0.1.0.0 |  | Store today's date on the company model.
[delivery_carrier_combine_price_rule](delivery_carrier_combine_price_rule/) | 12.0.1.0.0 |  | Chose how to combine price rule on a delivery carrier.
[delivery_product_restriction](delivery_product_restriction/) | 12.0.1.0.0 |  | Allow some product to be shipped only by some delivery carrier.
[document_hosting](document_hosting/) | 12.0.1.0.0 |  | Manage documents that can be published on website with ??.
[email_template_config](email_template_config/) | 12.0.1.0.0 |  | This module extends the email in order to force some behaviours configured in the mail template(e.g. force send mail or not).
[hr_holidays_custom_duration](hr_holidays_custom_duration/) | 12.0.1.0.1 |  | Allow to override the duration of a leave.
[invoice_global_discount](invoice_global_discount/) | 12.0.1.1.0 |  | This module give global discount on invoice. It allows to set the same discount on all the invoice lines without been forced to go manually through them.
[mail_activity_filter_internal_user](mail_activity_filter_internal_user/) | 12.0.1.0.1 |  | Filter on internal user by default when assigning someone to an activity.
[mail_auto_resend](mail_auto_resend/) | 12.0.1.0.0 |  | Automatically resend failed emails
[mrp_unbuild_product_mo_filter](mrp_unbuild_product_mo_filter/) | 12.0.1.0.1 |  | Filter unbuild manufacturing orders by selected product
[partner_contact_address](partner_contact_address/) | 12.0.1.0.0 |  | This module allows to have company contacts with their own address.
[partner_socialmedia](partner_socialmedia/) | 12.0.1.0.0 |  | Add social media fields to contacts
[partner_warehouse](partner_warehouse/) | 12.0.1.0.0 |  | Let the warehouse of the sale order be set accordingly to a default warehouse set on the partner.
[pos_auto_invoice](pos_auto_invoice/) | 12.0.1.0.0 |  | In the POS, set orders as to-invoice by default.
[pos_auto_invoice_default_partner](pos_auto_invoice_default_partner/) | 12.0.1.0.0 |  | Compatibility layer between pos_auto_invoice and pos_default_partner.
[pos_custom_receipt](pos_custom_receipt/) | 12.0.1.0.0 |  | Hide company's email and add customer's name to POS receipt
[pos_customer_wallet](pos_customer_wallet/) | 12.0.1.1.0 |  | Enable usage of the Customer Wallet in the Point of Sale.
[pos_customer_wallet_partner_is_user](pos_customer_wallet_partner_is_user/) | 12.0.1.1.0 | [![coopiteasy](https://github.com/coopiteasy.png?size=30px)](https://github.com/coopiteasy) | Add a field on partners that shows whether they have used customer wallet functionality, and don't show some parts of customer wallet functionality to partners who haven't already used it.
[pos_self_service_base](pos_self_service_base/) | 12.0.1.0.0 |  | POS Self-Service Base Module
[pos_self_service_print_zpl](pos_self_service_print_zpl/) | 12.0.1.0.0 |  | POS Self-Service Print ZPL from browser
[product_label_report](product_label_report/) | 12.0.1.0.0 |  | This module allows to show the print barcode and name of the product.
[product_to_bizerba_scale](product_to_bizerba_scale/) | 12.0.1.0.0 |  | This module merges product_to_scale_bizerba and product_to_scale_bizerba_extended into one.
[purchase_invoice_status](purchase_invoice_status/) | 12.0.1.0.0 |  | Add invoice status on purchase orders
[purchase_order_line_auto_import](purchase_order_line_auto_import/) | 12.0.1.0.0 |  | This module allows to create automatically line with the product and minimal quantities when selecting the partner.
[purchase_order_weight](purchase_order_weight/) | 12.0.1.0.0 |  | Adds weight and weight unit to Purchase Order
[report_certisys_label](report_certisys_label/) | 12.0.1.0.0 |  | Add Certisys Label on account, stock and sale reports
[resource_work_time_from_contracts](resource_work_time_from_contracts/) | 12.0.1.0.0 |  | Take the contracts of an employee into account when computing work time per day
[sale_order_for_approval](sale_order_for_approval/) | 12.0.1.0.0 |  | Display "For Approval" mention on Sale Orders
[sale_order_mass_confirmation](sale_order_mass_confirmation/) | 12.0.1.0.0 |  | Confirm multiple sale orders (quotations) with one action
[sale_order_volume](sale_order_volume/) | 12.0.1.1.1 |  | Computes the volume of products per category ordered and display it on
[sale_report_partner_category](sale_report_partner_category/) | 12.0.1.0.1 |  | Add a category field to sale reports
[stock_inventory_confirm_reset_qty](stock_inventory_confirm_reset_qty/) | 12.0.1.0.0 |  | Show a confirmation dialog box when clicking on 'Set quantities to 0' in a stock.inventory
[stock_picking_copy_qty](stock_picking_copy_qty/) | 12.0.1.0.0 |  | Adds a button to copy reserved quantity to received quantity
[stock_picking_only_suppliers_products](stock_picking_only_suppliers_products/) | 12.0.1.0.0 |  | On a stock picking, only display the supplier's products.
[stock_product_weight_on_receipt](stock_product_weight_on_receipt/) | 12.0.1.0.0 |  | Show product weight and unit weight on each line of a receipt
[stock_provider_ref_on_receipt](stock_provider_ref_on_receipt/) | 12.0.1.0.0 |  | Show provider reference on each line of a receipt
[web_m2x_options_no_partner](web_m2x_options_no_partner/) | 12.0.1.0.1 |  | Removes creation options from (some) partner dropdown menus.
[web_m2x_options_no_product](web_m2x_options_no_product/) | 12.0.1.0.1 |  | Removes creation options from (some) product dropdown menus.
[website_sale_delivery_vat_label](website_sale_delivery_vat_label/) | 12.0.1.0.0 |  | Display the included/excluded VAT label on delivery method
[website_sale_detailed_product_description](website_sale_detailed_product_description/) | 12.0.1.0.0 |  | Adds fields to Product Template and e-commerce's product list and page.
[website_sale_product_display_unit](website_sale_product_display_unit/) | 12.0.1.0.0 |  | Display the price per unit on the e-commerce pages.
[website_sale_product_weight](website_sale_product_weight/) | 12.0.1.0.0 |  | Display the weight of a product on the e-commerce product page.
[website_sale_sort_variants_by_availability](website_sale_sort_variants_by_availability/) | 12.0.1.0.0 |  | Sort the selection of product variants in e-commerce such that available ones are always displayed first.

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license. Consult each module's
`__manifest__.py` file, which contains a `license` key that explains its
license.
