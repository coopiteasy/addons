Wholesale business in the food sector sell their products by boxes or pallets. However the unit price must make sense, since this is the price that is useful for the customers (grocery stores).
In Odoo, one way to sell products by boxes is with units of measures (e.g. box of 6 units). Another way is with the packaging functionality, but to our knowledge there is no e-commerce functionality for packaging in Odoo so far.
In this case, the cost of the product is the cost of the box, and the sales price is computed based on this cost. If we want to convert the box price to sales price, this leads to prices with more than 2 decimals. When we round this price and we multiply it back by the box quantity we get a different sales price. Therefore this leads to unit sales prices which are inconsistent with box sales price. 

This module solves this problem by computing the sales price differently. The computation is based on the unit cost, which is the cost of the product divided by the factor ratio (box quantity) of it's unit of measure. This computes the unit sales price, which is then multiplied by the factor ratio to get the box sales price.
This way the unit price makes sense.

For instance, a wine product is sold by the wholesale business by boxes of 12. The cost of a box is 23,76€.

With the product_margin_classification module alone, the wholesale applies a margin of 1,28, this gives a sales price of 23,76€*1,28=30,41€ (rounded 2 decimals). The unit price is then 30,41€/12=2,53 (rounded 2 decimals)
However if we multiply the rounded unit price by 12, we get 30,36€. This is inconsistent with the sales price of 30,41€.


With this module, the unit cost is 23,76€/12=1,98€. The unit sales price is 1,98€*1,28=2,53€ (rounded two decimals). The box sales price is 2,53€*12 = 30,36€.
The box price is consistent with the unit price. 
