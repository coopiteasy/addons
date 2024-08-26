The number of work hours in a day is taken from the ``hours_per_day`` field of
the work schedule (``resource.calendar``). This field is automatically
computed when work intervals are edited, but its value can also be set
manually.

It is useful to set it manually in case of work schedules with irregular days.
For example, a work schedule of 8 hours per day for 4 days and 4 hours for 1
day should have its ``hours_per_day`` set to 8. This way, the total work time
for a week (used to compute leaves, for example) is exactly 4.5 days.
