Prevent loop between ``product_contract`` and ``contract_sale_generation``.

When using both the ``product_contract`` and the ``contract_sale_generation`` modules, a sale order generated from a contract will create another contract on confirmation.
This module prevents this from happening.

Without this module, a sale order with a product having ``is_contract`` as true, when confirmed, creates a contract.
This contract contains the same product (with ``is_contract`` as true).
If this contract is set to generate sale orders, then it will generate sale orders with this same product.
When these sale order are confirmed, they will create a contract, and so on.

With this module installed, this loop is broken: if a sale order was generated from a contract, confirming it will not create a new contract.
