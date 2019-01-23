# -*- coding: utf-8 -*-
from openerp import api, fields, models


class Task(models.Model):
    _inherit = 'project.task'

    has_contract_hours = fields.Boolean(string="Has contract hours",
                                        compute="_compute_has_contract_hours")

    remaining_contract_hours = fields.Float(
        string="Remaining Contract Hours",
        compute='_compute_remaining_hours_contract',
        digits=(16, 2))

    def _get_qty_invoiced(self):
        sale_order_lines = self.env['sale.order.line'].search(
            [('project_id', '=', self.analytic_account_id.id)])

        return sum([line.qty_invoiced for line in sale_order_lines])

    def _get_qty_effective(self):
        tasks = self.project_id.task_ids

        return sum([task.effective_hours for task in tasks])

    @api.multi
    @api.depends('remaining_hours')
    def _compute_remaining_hours_contract(self):
        _qty_invoiced = self._get_qty_invoiced()
        if _qty_invoiced > 0:
            for task in self:
                task.remaining_contract_hours = _qty_invoiced \
                                                - self._get_qty_effective()

    @api.multi
    @api.depends('has_contract_hours')
    def _compute_has_contract_hours(self):
        sale_order_lines = self.env['sale.order.line'].search(
            [('project_id', '=', self.analytic_account_id.id)])

        self.has_contract_hours = (sum(
            [line.qty_invoiced for line in sale_order_lines])) > 0
