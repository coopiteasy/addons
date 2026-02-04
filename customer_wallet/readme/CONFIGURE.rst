Setting this up requires a few careful steps:

- Make sure your user has access to all accounting features.

- Create an account (Customer Wallet) that is a liability.

  .. figure:: ../static/description/configure_account_account.png

In France, the account generally used will be "4197" - "Clients – Autres avoirs".

- Create a journal (Customer Wallet). Enable the 'Customer Wallet Journal'
  toggle, set the Bank Account to the previously created account, and in the
  payment methods (both incoming and outgoing), set the Outstanding Receipts and
  Outstanding Payments accounts to the previously created account. You may need
  to toggle the visibility of these fields in the tables.

  .. figure:: ../static/description/configure_account_journal.png

- In the Invoicing settings, set the Customer Wallet Account to the previously
  created account.

  .. figure:: ../static/description/configure_res_config_settings.png

- (Optional) Create a product (Wallet Product), and enable the Wallet Product
  toggle. The income and expense account will be automatically the Customer
  wallet account previously created.

  .. figure:: ../static/description/configure_product_template.png

