Setting this up requires a few careful steps:

1. Make sure your user has access to all accounting features.
2. Create an account (Customer Wallet) that is a liability.

   .. figure:: ../static/description/configure_account_account.png

   In France, the account generally used will be "4197" - "Clients – Autres
   avoirs".
3. Create a journal (Customer Wallet) of type “Bank”. Enable the “Customer
   Wallet Journal” toggle, set the Bank Account to the previously created
   account, and in the payment methods (both incoming and outgoing), set the
   Outstanding Receipts and Outstanding Payments accounts to the previously
   created account. You may need to toggle the visibility of these fields in
   the tables.

   .. figure:: ../static/description/configure_account_journal.png
4. In the Invoicing settings, set the Customer Wallet Account to the previously
   created account.

   .. figure:: ../static/description/configure_res_config_settings.png
5. (Optional) Create a product (Wallet Product), and enable the Wallet Product
   toggle. The income and expense accounts will be automatically set to the
   Customer Wallet Account previously created.

   .. figure:: ../static/description/configure_product_template.png
