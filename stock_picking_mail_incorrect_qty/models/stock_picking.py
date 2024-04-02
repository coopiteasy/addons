# Copyright 2021 Coop IT Easy SC
#   Carmen Bianca Bakker <carmen@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.tools.translate import _


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
        # The following code between the 'fmt' tags is copied almost-verbatim
        # from the stock module. It handles a corner case of move.lines being
        # unlinked to moves, but linked to stock.picking. It is copied here
        # verbatim because not including it would (potentially) result in some
        # moves being skipped over.
        #
        # The order of operations we want:
        #
        # - Copied code snippet below from stock_picking.action_done(). This
        #   fixes discrepancies as described.
        # - Send e-mail
        # - The remainder of stock_picking.action_done(). This function
        #   'destroys' the information that is needed for composing the e-mail
        #   (e.g., empty moves are cancelled, quantities are split and adjusted,
        #   etc etc etc).
        #
        # If we do the following order:
        #
        # - Send e-mail
        # - All of stock_picking.action_done()
        #
        # ... then the e-mailing functionality may not have access to the fixed
        # discrepancies.
        #
        # Further discussed and described in
        # <https://github.com/coopiteasy/addons/pull/192>.

        # flake8: noqa
        # fmt: off
        # Check if there are ops not linked to moves yet
        for pick in self:
            # # Link existing moves or add moves when no one is related
            for ops in pick.move_line_ids.filtered(lambda x: not x.move_id):
                # Search move with this product
                moves = pick.move_lines.filtered(lambda x: x.product_id == ops.product_id)
                moves = sorted(moves, key=lambda m: m.quantity_done < m.product_qty, reverse=True)
                if moves:
                    ops.move_id = moves[0].id
                else:
                    new_move = self.env['stock.move'].create({
                                                    'name': _('New Move:') + ops.product_id.display_name,
                                                    'product_id': ops.product_id.id,
                                                    'product_uom_qty': ops.qty_done,
                                                    'product_uom': ops.product_uom_id.id,
                                                    'location_id': pick.location_id.id,
                                                    'location_dest_id': pick.location_dest_id.id,
                                                    'picking_id': pick.id,
                                                    'picking_type_id': pick.picking_type_id.id,
                                                   })
                    ops.move_id = new_move.id
                    new_move = new_move._action_confirm()
                    # todo_moves |= new_move
                    #'qty_done': ops.qty_done})
        # fmt: on

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
        PosOrder = self.env.get("pos.order")
        for picking in self:
            # This function is indirectly called by the POS without defining
            # reserved availability for moves. Let's simply not send any mails for
            # pickings done by the POS.
            if PosOrder and PosOrder.search([("name", "==", record.origin)]):
                continue
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
