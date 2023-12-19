Take the contracts of an employee into account when computing work time per
day.

When this module is installed, the number of hours an employee is supposed to
work is only computed from their contracts. Without contracts, the work time
per day is 0, instead of using the default company’s working hours.

The start and end dates of contracts are taken into account, but the status
(state) of contracts are ignored.

For this module to work properly, the company’s working hours should encompass
all possible work days (including weekend days if there are contracts with
weekend days), and each day should have working hours that correspond to the
working hours used in all contracts. This is because the company’s working
hours are used to compute leaves, and the number of hours per day is computed
from it.

For example, if the company working hours define 8 hours per day, from 8 to 12
and 13 to 17, all contracts’ working hours should be set from 8 to 12 and/or
from 13 to 17 for the corresponding days. Half days are thus supported.

If there are contracts with working hours that don’t match the company’s
working hours, the number of days for leaves will be computed incorrectly.

This module also makes the working hours (resource calendar) of an employee
always equal to the company’s working hours, and hides its field on the
employee form view.
