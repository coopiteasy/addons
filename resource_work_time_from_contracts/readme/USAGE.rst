The number of work hours in a day is taken from the ``hours_per_day`` field of
the work schedule (``resource.calendar``). This field is automatically
computed when work intervals are edited, but its value can also be set
manually.

It is useful to set it manually in case of work schedules with irregular days.
For example, a work schedule of 8 hours per day for 4 days and 4 hours for 1
day should have its ``hours_per_day`` set to 8. This way, the total work time
for a week (used to compute leaves, for example) is exactly 4.5 days.

It is possible to control the rounding of the computed number of days. This
can be useful for work schedules with irregular days, where some days have
durations that don't match common divisions of a full day.

The rounding mode is controlled by the
``resource_work_time_from_contracts.day_rounding_mode`` system parameter
(``ir.config_parameter``). Here are its supported values:

* ``none``: No rounding is done. This is the default.
* ``round``: Round to the nearest unit.
* ``ceil``: Round to the next unit above the value.

For the ``round`` and ``ceil`` modes, the
``resource_work_time_from_contracts.day_rounding_granularity`` system
parameter defines the unit to which to round values. The default value is
``1``, which means to round to full days. Setting it to ``0.5``, for example,
will round to half days.

There is currently no custom view to configure these settings. They must be
set manually using the System Parameters view from the Technical Settings menu
(accessible by enabling the developer mode).
