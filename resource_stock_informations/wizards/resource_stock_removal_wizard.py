# Copyright 2021 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


from openerp import api, fields, models, _
from openerp.exceptions import ValidationError


class StockRemovalWizard(models.TransientModel):
    _name = "resource.stock.removal.wizard"
    _description = "Resource Stock Removal Wizard"

    resource_id = fields.Many2one(
        comodel_name="resource.resource",
        string="Resource",
        required=True,
    )
    stock_removal_date = fields.Date(
        string="Stock Removal Date", default=lambda _: fields.Date.today()
    )
    stock_removal_reason = fields.Selection(
        string="Stock Removal Reason",
        selection=[
            ("sold", "Sold"),
            ("stolen", "Stolen"),
            ("given", "Given"),
            ("broken", "Broken"),
            ("other", "Other"),
        ],
    )
    selling_price = fields.Float(string="Selling Price")
    sale_invoice_ref = fields.Char(string="Sale Invoice Ref")

    allocations_to_fix_ids = fields.Many2many(
        comodel_name="resource.allocation",
        string="Allocations to Fix",
        compute="_compute_allocations_to_fix",
    )
    _has_allocations_to_fix = fields.Boolean(
        string="Has Allocations to Fix",
        compute="_compute_allocations_to_fix",
    )
    candidate_resource_ids = fields.Many2many(
        comodel_name="resource.resource",
        string="Candidate Resources",
        compute="_compute_candidate_resource_ids",
    )
    _has_candidates = fields.Boolean(
        string="Has Candidates",
        compute="_compute_candidate_resource_ids",
    )
    replacing_resource_id = fields.Many2one(
        comodel_name="resource.resource",
        string="Replacing Resource",
    )
    force_remove = fields.Boolean(
        "No resources available to fix allocations. Remove anyway ?"
    )

    @api.multi
    def button_remove_resource_from_stock(self):
        self.ensure_one()

        self.remove_resource_from_stock()

    @api.multi
    def button_remove_resource_from_stock_and_fix_allocations(self):
        self.ensure_one()
        self.fix_allocations()
        self.remove_resource_from_stock()

    @api.multi
    def remove_resource_from_stock(self):
        self.ensure_one()

        if not self.stock_removal_reason:
            raise ValidationError(
                _(
                    "Please provide a reason for the resource removal from "
                    "stock "
                )
            )

        if self.allocations_to_fix_ids and not self.force_remove:
            raise ValidationError(
                _(
                    "You must first fix existing allocations "
                    "before removing %s from the stock"
                )
                % self.resource_id.name
            )

        self.resource_id.write(
            {
                "removed_from_stock": True,
                "state": "unavailable",
                "stock_removal_date": self.stock_removal_date,
                "stock_removal_reason": self.stock_removal_reason,
                "selling_price": self.selling_price,
                "sale_invoice_ref": self.sale_invoice_ref,
            }
        )

    @api.multi
    def fix_allocations(self):
        self.ensure_one()

        if not self.replacing_resource_id:
            raise ValidationError(
                _("Please select a resource to replace %s")
                % self.resource_id.name
            )

        self.allocations_to_fix_ids.write(
            {"resource_id": self.replacing_resource_id.id}
        )

    def _get_candidate_resources(self):
        self.ensure_one()
        date_clause_template = (
            "("
            "(ra.date_start between '{date_start}' and '{date_end}')"
            " or "
            "(ra.date_end between '{date_start}' and '{date_end}')"
            ")"
        )
        if self.allocations_to_fix_ids:
            join_date_clause = " or ".join(
                (
                    date_clause_template.format(
                        date_start=a.date_start, date_end=a.date_end
                    )
                    for a in self.allocations_to_fix_ids
                )
            )
            join_date_clause = "and (%s)" % join_date_clause
        else:
            join_date_clause = ""

        query = """
select rr.id
from resource_resource rr
         left join resource_allocation ra on rr.id = ra.resource_id
    and ra.state != 'cancel'
    {join_date_clause}
where rr.location = %(location_id)s
    and rr.category_id = %(category_id)s
    and rr.id != %(resource_id)s
    and rr.state = 'available'
    and ra.id is null
        """
        self.env.cr.execute(
            query.format(join_date_clause=join_date_clause),
            {
                "location_id": self.resource_id.location.id,
                "category_id": self.resource_id.category_id.id,
                "resource_id": self.resource_id.id,
            },
        )
        resource_ids = [x for x, in self.env.cr.fetchall()]
        return self.env["resource.resource"].browse(resource_ids)

    @api.multi
    @api.depends("resource_id.allocations.resource_id")
    def _compute_allocations_to_fix(self):
        for wiz in self:
            wiz.allocations_to_fix_ids = wiz.resource_id.allocations.filtered(
                lambda ra: ra.date_start >= fields.Datetime.now()
                and ra.state != "cancel"
            )
            wiz._has_allocations_to_fix = bool(wiz.allocations_to_fix_ids)

    @api.multi
    @api.depends("resource_id")
    def _compute_candidate_resource_ids(self):
        for wiz in self:
            wiz.candidate_resource_ids = wiz._get_candidate_resources()
            wiz._has_candidates = bool(wiz.candidate_resource_ids)

    @api.onchange("stock_removal_reason")
    def onchange_stock_removal_reason(self):
        """set domain for replacing resource"""
        domain = [("id", "in", self.candidate_resource_ids.ids)]
        return {"domain": {"replacing_resource_id": domain}}
