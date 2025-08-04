This module adds the following fields to the purchase order products quick add
view (from the ``purchase_quick`` module):

- minimum quantity (from the ``product_main_supplier`` module)
- purchase unit of measure

Minimum purchase quantity is computed from the main
supplier of the product. It might not be matching with the
selected producer if the product has several suppliers.
