from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    correction = fields.Boolean("Correction Mode", copy=False)
    invoice_line_ids = fields.One2many(readonly=False)
    tax_line_ids = fields.One2many(readonly=False)
    account_id = fields.Many2one(readonly=False)
    origin_account_id = fields.Many2one("account.account", readonly=True)

    @api.model_cr
    def init(self):
        res = super(AccountInvoice, self).init()
        self._cr.execute(
            "UPDATE account_invoice "
            "SET origin_account_id = account_id "
            "WHERE state in ('open', 'paid') AND origin_account_id IS NULL;"
        )
        return res

    @api.multi
    def write(self, vals):
        price_per_id = {rec.id: rec.amount_total for rec in self}

        res = super(AccountInvoice, self).write(vals)
        for rec in self:
            if (
                rec.state in ["open", "paid"]
                and float_compare(
                    rec.amount_total,
                    price_per_id[rec.id],
                    precision_rounding=rec.currency_id.rounding,
                )
                != 0
            ):
                raise ValidationError(
                    _("You cannot change the amount of a " "validated invoice")
                )
        return res

    @api.multi
    def invoice_validate(self):
        """ Overwrite to keep track of the account_id set at validation """
        for rec in self:
            rec.origin_account_id = rec.account_id
        return super(AccountInvoice, self).invoice_validate()

    @api.multi
    def start_correction(self):
        self.ensure_one()
        if not self.env.user.has_group("account.group_account_manager"):
            raise UserError(
                _(
                    "Only Account/ Adviser user can start the "
                    "correction of an invoice"
                )
            )
        self.correction = True

    @api.multi
    def validate_correction(self):
        self.ensure_one()
        if not self.env.user.has_group("account.group_account_manager"):
            raise UserError(
                _(
                    "Only Account/ Adviser user can validate the "
                    "correction of an invoice"
                )
            )
        main_move = self.env["account.move.line"]
        to_delete_move = self.env["account.move.line"]
        for move_line in self.move_id.line_ids:
            if move_line.account_id == self.origin_account_id:
                main_move |= move_line
            else:
                to_delete_move |= move_line

        # 1 Move in draft and reconcile entry inactive
        reconcile = self.move_id.line_ids.mapped(
            "matched_debit_ids"
        ) | self.move_id.line_ids.mapped("matched_credit_ids")
        reconcile.write({"active": False})
        self.invalidate_cache()
        self.move_id.write({"state": "draft"})
        # 2 Main move change account_id
        main_move.write({"account_id": self.account_id.id})
        # 3 prepare line to delete
        m2m_command = [(2, rec.id, 0) for rec in to_delete_move]
        # 4 prepate line to create
        iml = self.invoice_line_move_line_get() + self.tax_line_move_line_get()
        _a, _b, iml = self.compute_invoice_totals(self.company_id.currency_id, iml)
        part = self.env["res.partner"]._find_accounting_partner(self.partner_id)
        line = [(0, 0, self.line_get_convert(l, part.id)) for l in iml]
        line = self.group_lines(iml, line)
        line = self.finalize_invoice_move_lines(line)
        m2m_command += line
        self.move_id.with_context(
            check_move_validity=False, dont_create_taxes=True
        ).write({"line_ids": m2m_command})
        # 5 Back to posted
        reconcile.write({"active": True})
        self.invalidate_cache()
        self.move_id.write({"state": "posted"})
        # 6 Clean correction
        self.write({"origin_account_id": self.account_id.id, "correction": False})


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    correction = fields.Boolean(related="invoice_id.correction", readonly=True)
    state = fields.Selection(related="invoice_id.state", default="draft")
    # Make all these fields readonly when the invoice is not in draft
    price_unit = fields.Float(readonly=True, states={"draft": [("readonly", False)]})
    product_id = fields.Many2one(readonly=True, states={"draft": [("readonly", False)]})
    name = fields.Char(readonly=True, states={"draft": [("readonly", False)]})
    quantity = fields.Float(readonly=True, states={"draft": [("readonly", False)]})

    @api.multi
    def write(self, vals):
        price_per_id = {rec.id: rec.price_subtotal for rec in self}
        res = super(AccountInvoiceLine, self).write(vals)
        for rec in self:
            if (
                rec.state in ["open", "paid"]
                and float_compare(
                    rec.price_subtotal,
                    price_per_id[rec.id],
                    precision_rounding=rec.currency_id.rounding,
                )
                != 0
            ):
                raise ValidationError(
                    _("You cannot change the amount of a validated invoice")
                )
        return res

    @api.multi
    def unlink(self):
        if any([s in ["open", "paid"] for s in self.mapped("state")]):
            raise ValidationError(
                _("You cannot delete a invoice line from a confirmed invoice")
            )
        return super(AccountInvoiceLine, self)


class AccountPartialReconcile(models.Model):
    _inherit = "account.partial.reconcile"

    active = fields.Boolean(default=True)
