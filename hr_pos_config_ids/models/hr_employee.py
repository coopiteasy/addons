from odoo import fields, models


class HrEmployeeBase(models.AbstractModel):
    _inherit = "hr.employee.base"

    pos_config_ids = fields.Many2many(
        "pos.config",
        relation="hr_employee_pos_config_rel",
        column1="hr_employee_id",
        column2="pos_config_id",
        string="PoS that this employee has access to",
        domain=[("module_pos_hr", "=", True)],
    )


class EmployeePublic(models.Model):
    _inherit = "hr.employee.public"

    pos_config_ids = fields.Many2many(readonly=True)
