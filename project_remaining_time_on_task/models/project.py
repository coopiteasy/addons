# -*- coding: utf-8 -*-
from openerp import api, fields, models


class Task(models.Model):
    _inherit = 'project.task'

    remaining_contract_hours = fields.Float(string="Remaining contract hours",
                                            compute='_compute_remaining_hours_contract',
                                            digits=(16, 2))

    def _get_qty_invoiced(self):
        _qty_invoiced = 0
        sale_order_lines = self.env['sale.order.line'].search(
            [('project_id', '=', self.analytic_account_id.id)])
        for line in sale_order_lines:
            _qty_invoiced += line.qty_invoiced

        return _qty_invoiced

    def _get_qty_effective(self):
        _qty_effective = 0
        tasks = self.project_id.task_ids
        for task in tasks:
            _qty_effective += task.effective_hours

        return _qty_effective

    @api.multi
    @api.depends('remaining_hours')
    def _compute_remaining_hours_contract(self):
        _qty_invoiced = self._get_qty_invoiced()
        if _qty_invoiced > 0:
            for task in self:
                task.remaining_contract_hours = _qty_invoiced - self._get_qty_effective()
