Sequence of Operations
~~~~~~~~~~~~~~~~~~~~~~

The exact sequence in which Customer Wallet operations done in the same PoS session are done is not stored and cannot be correctly recomputed.
For example, if a customer first credits their wallet in one order, then uses their wallet to pay for another order, these operations may appear in a different sequence when displaying the wallet details, possibly yielding a (falsely) negative balance at some point.

This is because all ``account.move.line`` records of a PoS session are created when closing the session and have thus the same value for their ``date`` and ``create_date`` fields.
Although ``pos.order`` records have a ``date_order`` field which is of type ``Datetime``, there is no link between ``account.move.line`` and ``pos.order`` records, so it cannot be retrieved.
Moreover, as some ``account.move.line`` records (specific to Customer Wallet operations) are deleted and others created when closing the PoS session, the ``id`` field cannot be used as a sorting field either.
