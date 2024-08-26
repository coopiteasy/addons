Take the contracts of an employee into account when computing work time per
day.

When this module is installed, the number of hours an employee is supposed to
work is only computed from their contracts. Without contracts, the work time
per day is 0, instead of using the default work schedule of the company.

The start and end dates of contracts are taken into account, but the status
(state) of contracts are ignored.

This module also makes the work schedule (``resource.calendar``) of an
employee always equal to the work schedule of the company, and hides its field
on the employee form view. This is because this work schedule is only used to
store all the leaves (``resource.calendar.leaves``) of all employees and is
otherwise ignored.
