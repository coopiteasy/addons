# Copyright 2021 Coop IT Easy SCRL fs
#   Carmen Bianca Bakker <carmen@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class Picking(models.Model):
    _inherit = "stock.picking"

    zero_received_move_ids = fields.One2many(
        "stock.move",
        string="Stock moves that were not received",
        compute="_compute_move_discrepancy",
    )
    zero_expected_move_ids = fields.One2many(
        "stock.move",
        string="Stock moves of which some were received, but none were expected",
        compute="_compute_move_discrepancy",
    )
    too_few_received_move_ids = fields.One2many(
        "stock.move",
        string="Stock moves of which too few were received",
        compute="_compute_move_discrepancy",
    )
    too_many_received_move_ids = fields.One2many(
        "stock.move",
        string="Stock moves of which too many were received",
        compute="_compute_move_discrepancy",
    )

    @api.multi
    @api.depends("move_lines")
    def _compute_move_discrepancy(self):
        for picking in self:
            # The following filter is also used in upstream action_done()
            filtered_moves = picking.mapped("move_lines").filtered(
                lambda move: move.state
                in [
                    "draft",
                    "waiting",
                    "partially_available",
                    "assigned",
                    "confirmed",
                ]
            )

            picking.zero_received_move_ids = filtered_moves.filtered(
                lambda move: move.quantity_done == 0 and move.reserved_availability
            )
            picking.zero_expected_move_ids = filtered_moves.filtered(
                lambda move: move.quantity_done and move.reserved_availability == 0
            )
            picking.too_few_received_move_ids = filtered_moves.filtered(
                lambda move: move.quantity_done != 0
                and move.quantity_done < move.reserved_availability
            )
            picking.too_many_received_move_ids = filtered_moves.filtered(
                lambda move: move.quantity_done > move.reserved_availability
                and move.reserved_availability != 0
            )

    @api.multi
    def action_done(self):
        self._notify_incorrect_delivery()

        return super(Picking, self).action_done()

    @api.multi
    def form_view_url(self):
        self.ensure_one()
        return "{}/web#id={}&model=stock.picking&view_type=form".format(
            self.env["ir.config_parameter"].sudo().get_param("web.base.url"),
            self.id,
        )

    @api.multi
    def _notify_incorrect_delivery(self):
        """Send a notification e-mail about the incorrect delivery."""
        for picking in self:
            if any(
                (
                    picking.zero_received_move_ids,
                    picking.zero_expected_move_ids,
                    picking.too_few_received_move_ids,
                    picking.too_many_received_move_ids,
                )
            ):
                self.env.ref(
                    "stock_picking_mail_incorrect_qty.mail_template_incorrect_delivery"
                ).send_mail(picking.id)

        return True
