This module allows to edit the duration (number of days) of a leave. This
allows to override the automatically-computed value.

**Limitations**

If a leave type is configured to use hours instead of days, the number of
hours displayed will be incorrect. They will still show the
automatically-computed value instead of the actual value. Internally, all
leaves are computed as days, so the actual value will still be correct.
