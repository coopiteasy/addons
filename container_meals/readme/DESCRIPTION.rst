This module supports a very specific business model, where customers get meals
delivered to them in glass containers. The containers are lent out and must be
returned. The customers pay a deposit on the glass containers, which they can
have refunded, or which gives them an effective perpetual discount on subsequent
purchases, where they don't have to pay the deposit on the glass containers
again.

Each meal comes in two glass containers. When two of the same meal are ordered,
those two meals also come in two glass containers total, but the glass
containers may be bigger to account for the increased volume.

This module:

- Creates an "Is Meal?" button for meal products, which enables the user to set
  the volumes of a single portion for containers 1 and 2.
- Adds a portion size product category. Child portions have 2/3 the volume of
  adult portions. This module does not adjust the price of child portions.
- Adds an "Is Container?" button for container products, which enables the user
  to set the volume of the container.
- Keeps track of the built up deposit by customers across sales.
- Allows the user to set unreturned containers on sale orders. All containers
  are assumed to be returned, and must be manually flagged as unreturned.
  Unreturned containers can be found on a customer's contact view and in a
  special "Unreturned Containers" menu under Sales.
- Calculates and automatically adds the containers needed to hold the
  to-purchase meals on the purchase page, and applies a discount depending on
  the customer's current stored deposit.
