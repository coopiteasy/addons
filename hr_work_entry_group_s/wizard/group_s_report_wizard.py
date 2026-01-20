# SPDX-FileCopyrightText: 2026 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import base64
import logging
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime

from dateutil.relativedelta import relativedelta

from odoo import _, fields, models
from odoo.exceptions import UserError, ValidationError

logger = logging.getLogger(__name__)


@dataclass
class FieldFormatter:
    name: str  # Output field name
    length: int or tuple(int)  # Length of the field
    formatter: Callable  # Function to format the value


class GroupSReportWizard(models.TransientModel):
    _name = "group.s.report.wizard"
    _description = "Wizard to generate the group S work entries report"

    employee_ids = fields.Many2many(
        comodel_name="hr.employee", string="Selected Employees"
    )
    # Default is the 1st day of the previous month
    date_start = fields.Date(
        "Start Date",
        required=True,
        default=datetime.today().replace(day=1) - relativedelta(months=1),
    )
    # Default is the last day of the previous month
    date_stop = fields.Date(
        "End Date",
        required=True,
        default=datetime.today().replace(day=1) - relativedelta(days=1),
    )

    def action_generate_report(self):
        self.ensure_one()

        field_formatters = self._get_field_formatters()
        file_content = self.generate_report_content(field_formatters)
        file_data = base64.b64encode(file_content.encode("ascii"))
        report_name = self._get_report_name()

        attachment = self.env["ir.attachment"].create(
            {
                "name": report_name,
                "type": "binary",
                "datas": file_data,
                "res_model": self._name,
                "res_id": self.id,
                "mimetype": "text/plain",
            }
        )
        return {
            "type": "ir.actions.act_url",
            "url": f"/web/content/{attachment.id}?download=true",
            "target": "self",
        }

    def _get_report_name(self):
        social_secretariat_affiliation_number = self.pad_with_zeroes(
            self.env.company.social_secretariat_affiliation_number,
            6,
        )
        report_number = self.env.company.group_s_report_counter
        self.env.company.increment_group_s_report_counter()
        report_number = self.pad_with_zeroes(report_number, 3)
        report_name = f"SA{social_secretariat_affiliation_number}.{report_number}"
        return report_name

    def _get_field_formatters(self):
        field_formatters = (
            FieldFormatter(
                name="group_s_code", length=6, formatter=self._prepare_group_s_code
            ),
            FieldFormatter(name="date", length=6, formatter=self._prepare_date),
            FieldFormatter(name="code", length=9, formatter=self._prepare_code),
            FieldFormatter(name="team_code", length=1, formatter=self.pad_with_spaces),
            FieldFormatter(
                name="amount", length=(7, 2), formatter=self._prepare_amount
            ),
            FieldFormatter(
                name="unitary_value", length=(5, 4), formatter=self.pad_with_zeroes
            ),
            FieldFormatter(
                name="percentage", length=(3, 2), formatter=self.pad_with_zeroes
            ),
            FieldFormatter(
                name="analytical_center_fee", length=10, formatter=self.pad_with_spaces
            ),
            FieldFormatter(
                name="project_reference", length=6, formatter=self.pad_with_spaces
            ),
            FieldFormatter(
                name="activity_reference", length=5, formatter=self.pad_with_spaces
            ),
            FieldFormatter(
                name="reference_management_level",
                length=15,
                formatter=self.pad_with_zeroes,
            ),
            FieldFormatter(
                name="justification", length=1, formatter=self.pad_with_spaces
            ),
            FieldFormatter(name="reserve", length=1, formatter=self.pad_with_spaces),
            FieldFormatter(
                name="work_entry_code_2", length=9, formatter=self.pad_with_spaces
            ),
            FieldFormatter(
                name="km_mobility", length=5, formatter=self.pad_with_zeroes
            ),
            FieldFormatter(
                name="km_transport", length=5, formatter=self.pad_with_zeroes
            ),
            FieldFormatter(
                name="mobility_code", length=2, formatter=self.pad_with_spaces
            ),
            FieldFormatter(
                name="transport_code", length=2, formatter=self.pad_with_spaces
            ),
            FieldFormatter(name="days", length=5, formatter=self._prepare_days),
            FieldFormatter(name="hours", length=(8, 2), formatter=self._prepare_hours),
        )
        return field_formatters

    def pad_with_zeroes(self, field_value="", length=0):
        # If field_value is a model, it's probably an unprocessed work entry
        if isinstance(field_value, models.BaseModel):
            field_value = ""
        if isinstance(length, int):
            formatted_value = str(field_value).zfill(length)
            return formatted_value
        else:
            length_int, length_decimals = length
            if field_value:
                (value_int, value_decimals) = str(float(field_value)).split(".")
            else:
                value_int = 0
                value_decimals = 0
            formatted_value_int = str(int(value_int)).zfill(length_int)
            formatted_value_decimals = str(int(value_decimals)).rjust(
                length_decimals, "0"
            )
            return formatted_value_int + formatted_value_decimals

    def pad_with_spaces(self, field_value="", length=0):
        # If field_value is a model, it's probably an unprocessed work entry
        if isinstance(field_value, models.BaseModel):
            field_value = ""
        if isinstance(length, int):
            formatted_value = "{message: <{length}}".format(
                message=field_value, length=length
            )
            return formatted_value
        else:
            length_int, length_decimals = length
            formatted_value_int = "{message: <{length}}".format(
                message="", length=length_int
            )
            formatted_value_decimals = "{message: >{length}}".format(
                message="", length=length_decimals
            )
            return formatted_value_int + formatted_value_decimals

    def _prepare_group_s_code(self, work_entry, length):
        group_s_code = work_entry.contract_id.group_s_code
        if not group_s_code:
            raise ValidationError(
                _("'%s' doesn't have an attributed group S code")
                % (work_entry.employee_id.name)
            )
        group_s_code = self.pad_with_zeroes(group_s_code, length)
        return group_s_code

    def _prepare_date(self, work_entry, length):
        date = work_entry.date_start
        date = date.strftime("%y%m%d")
        return date

    def _prepare_code(self, work_entry, length):
        code = work_entry.external_code
        if not code:
            raise ValidationError(
                _("The work entry '%s' doesn't have an external code")
                % (work_entry.name)
            )
        code = self.pad_with_spaces(code, length)
        return code

    def _prepare_amount(self, work_entry, length):
        amount = self.pad_with_zeroes("", length)
        amount = "+" + amount
        return amount

    def _prepare_days(self, work_entry, length):
        td = work_entry.date_stop - work_entry.date_start
        return self.pad_with_zeroes(td.days, length)

    def _prepare_hours(self, work_entry, length):
        td = work_entry.date_stop - work_entry.date_start
        hours = td.seconds / 3600
        return self.pad_with_zeroes(hours, length)

    def generate_report_content(self, field_formatters):
        res = "VERSION 2\r\n"
        # makes sure the work entries are up to date
        [
            employee.generate_work_entries(self.date_start, self.date_stop)
            for employee in self.employee_ids
        ]
        work_entries = self.env["hr.work.entry"].search(
            [
                ("employee_id", "in", self.employee_ids.ids),
                ("date_start", ">=", self.date_start),
                ("date_stop", "<=", self.date_stop),
            ],
            order="employee_id, date_start, date_stop",
        )

        if not work_entries:
            raise UserError(_("No work entries found for the selected dates"))
        for work_entry in work_entries:
            line = ""
            for field_formatter in field_formatters:
                formatter = field_formatter.formatter
                length = field_formatter.length
                line += formatter(work_entry, length)
            line += "\r\n"
            res += line
        return res
