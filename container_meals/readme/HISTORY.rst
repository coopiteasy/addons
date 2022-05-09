14.0.1.1.0 (2022-05-09)
~~~~~~~~~~~~~~~~~~~~~~~

**Bugfixes**

- The deposit discount can now be greater than the price total of the containers
  in an order, but never greater than the total of the order itself. Previously,
  only the price total of the containers was given as a discount. (`#224 <https://github.com/coopiteasy/addons/issues/224>`_)
