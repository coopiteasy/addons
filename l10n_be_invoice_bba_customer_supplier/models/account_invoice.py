# Copyright 2009-2019 Noviat.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
import random
import re
import time

from odoo import _, api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    # this same field is also defined in OCA account_payment_order
    reference_type = fields.Selection(
        selection="_selection_reference_type",
        string="Payment Reference",
        required=True,
        default="none",
    )

    @api.model
    def _selection_reference_type(self):
        return [
            ("none", _("Free Communication")),
            ("bba", _("BBA Structured Communication")),
        ]

    def check_bbacomm(self, val):
        supported_chars = "0-9+*/ "
        pattern = re.compile("[^" + supported_chars + "]")
        if pattern.findall(val or ""):
            return False
        bbacomm = re.sub(r"\D", "", val or "")
        if len(bbacomm) == 12:
            base = int(bbacomm[:10])
            mod = base % 97 or 97
            if mod == int(bbacomm[-2:]):
                return True
        return False

    def duplicate_bba(self, partner, reference):
        """
        overwrite this method to customize the handling of
        duplicate BBA communications
        """
        if partner.out_inv_comm_algorithm == "random":
            # generate new bbacom to cope with duplicate bba coming
            # out of random generator
            reference = self.generate_bbacomm(partner)

        dups = self.search(
            [
                ("type", "=", "out_invoice"),
                ("state", "!=", "draft"),
                ("reference_type", "=", "bba"),
                ("reference", "=", reference),
            ]
        )
        if dups:
            raise UserError(
                _(
                    "The BBA Structured Communication "
                    "has already been used!"
                    "\nPlease use a unique BBA Structured Communication."
                )
            )
        return reference

    @api.constrains("reference_type", "reference")
    def _check_communication(self):
        for inv in self:
            if inv.reference_type == "bba":
                if not self.check_bbacomm(inv.reference):
                    raise UserError(
                        _("Invalid BBA Structured Communication !")
                    )

    @api.onchange("partner_id", "company_id")
    def _onchange_partner_id(self):
        res = super()._onchange_partner_id()
        partner = self.partner_id.commercial_partner_id
        if type == "out_invoice":
            self.reference_type = partner.out_inv_comm_type or "none"
            if self.reference_type == "bba":
                self.reference = self.generate_bbacomm(partner)
        return res

    @api.onchange("reference_type", "reference")
    def _onchange_reference_type(self):
        if self.type == "out_invoice":
            if self.reference_type == "bba":
                partner = self.partner_id.commercial_partner_id
                self.reference = self.generate_bbacomm(partner)

    def format_bbacomm(self, val):
        bba = re.sub(r"\D", "", val)
        bba = "+++{}/{}/{}+++".format(bba[0:3], bba[3:7], bba[7:])
        return bba

    def _generate_bbacomm_hook(self, partner, algorithm):
        """
        hook to add customer specific algorithm
        """
        raise Warning(
            _(
                "Unsupported Structured Communication Type "
                "Algorithm '%s' !"
                "\nPlease contact your Odoo support channel."
            )
            % algorithm
        )

    def generate_bbacomm(self, partner):
        algorithm = "random"
        if partner:
            algorithm = partner.out_inv_comm_algorithm or "random"
        else:
            partner = False

        if algorithm == "date":
            doy = time.strftime("%j")
            year = time.strftime("%Y")
            seq = "001"
            sequences = self.search(
                [
                    ("type", "=", "out_invoice"),
                    ("reference_type", "=", "bba"),
                    ("reference", "like", "+++{}/{}/%".format(doy, year)),
                ],
                order="reference",
            )
            if sequences:
                prev_seq = int(sequences[-1].reference[12:15])
                if prev_seq < 999:
                    seq = "%03d" % (prev_seq + 1)
                else:
                    raise Warning(
                        _(
                            "The daily maximum of outgoing invoices "
                            "with an automatically generated "
                            "BBA Structured Communication "
                            "has been exceeded!"
                            "\nPlease create manually a unique "
                            "BBA Structured Communication."
                        )
                    )
            bbacomm = doy + year + seq
            base = int(bbacomm)
            mod = base % 97 or 97
            reference = "+++%s/%s/%s%02d+++" % (doy, year, seq, mod)

        elif algorithm == "partner_ref":
            partner_ref = partner and partner.ref
            partner_ref_nr = re.sub(r"\D", "", partner_ref or "")
            if (len(partner_ref_nr) < 3) or (len(partner_ref_nr) > 7):
                raise Warning(
                    _(
                        "The Partner should have a 3-7 digit "
                        "Reference Number for the generation of "
                        "BBA Structured Communications!' \
                      '\nPlease correct the Partner record."
                    )
                )
            else:
                partner_ref_nr = partner_ref_nr.ljust(7, "0")
                seq = "001"
                sequences = self.search(
                    [
                        ("type", "=", "out_invoice"),
                        ("reference_type", "=", "bba"),
                        (
                            "reference",
                            "like",
                            "+++%s/%s/%%"
                            % (partner_ref_nr[:3], partner_ref_nr[3:]),
                        ),
                    ],
                    order="reference",
                )
                if sequences:
                    prev_seq = int(sequences[-1].reference[12:15])
                    if prev_seq < 999:
                        seq = "%03d" % (prev_seq + 1)
                    else:
                        raise Warning(
                            _(
                                "The daily maximum of outgoing "
                                "invoices with an automatically "
                                "generated BBA Structured "
                                "Communications has been exceeded!"
                                "\nPlease create manually a unique"
                                "BBA Structured Communication."
                            )
                        )
            bbacomm = partner_ref_nr + seq
            base = int(bbacomm)
            mod = base % 97 or 97
            reference = "+++%s/%s/%s%02d+++" % (
                partner_ref_nr[:3],
                partner_ref_nr[3:],
                seq,
                mod,
            )

        elif algorithm == "random":
            base = random.randint(1, 9999999999)
            bbacomm = str(base).rjust(10, "0")
            base = int(bbacomm)
            mod = base % 97 or 97
            mod = str(mod).rjust(2, "0")
            reference = "+++{}/{}/{}{}+++".format(
                bbacomm[:3], bbacomm[3:7], bbacomm[7:], mod
            )

        else:
            reference = self._generate_bbacomm_hook(partner, algorithm)

        return reference

    @api.model
    def _prepare_refund(
        self,
        invoice,
        date_invoice=None,
        date=None,
        description=None,
        journal_id=None,
    ):
        res = super()._prepare_refund(
            invoice,
            date_invoice=date_invoice,
            date=date,
            description=description,
            journal_id=journal_id,
        )
        res["reference_type"] = self.reference_type
        return res

    @api.model
    def create(self, vals):
        partner = self.env["res.partner"].browse(vals.get("partner_id"))
        partner = partner.commercial_partner_id
        if vals.get("type"):
            inv_type = vals.get("type")
        else:
            inv_type = self.env.context.get("type", "out_invoice")
            vals["type"] = inv_type
        reference_type = vals.get("reference_type")
        if not reference_type and inv_type == "out_invoice":
            reference_type = partner.out_inv_comm_type
        payref = vals.get("reference")

        if reference_type == "bba":
            if inv_type == "out_invoice":
                if not self.check_bbacomm(payref):
                    payref = self.generate_bbacomm(partner)
                    dups = self.search(
                        [
                            ("type", "=", "out_invoice"),
                            ("state", "!=", "draft"),
                            ("reference_type", "=", "bba"),
                            ("reference", "=", payref),
                        ]
                    )
                    if dups:
                        payref = self.duplicate_bba(partner, payref)
            else:
                if not payref:
                    raise UserError(
                        _(
                            "Empty BBA Structured Communication!"
                            "\nPlease fill in a "
                            "BBA Structured Communication."
                        )
                    )
                elif self.check_bbacomm(payref):
                    payref = self.format_bbacomm(payref)
            vals.update(
                {"reference_type": reference_type, "reference": payref}
            )
        return super().create(vals)

    @api.multi
    def write(self, vals):
        for inv in self:

            if inv.state == "draft":
                if "reference_type" in vals:
                    reference_type = vals["reference_type"]
                else:
                    reference_type = inv.reference_type
                if reference_type == "bba":
                    if "reference" in vals:
                        bbacomm = vals["reference"]
                    else:
                        bbacomm = inv["reference"] or ""
                    if self.check_bbacomm(bbacomm):
                        reference = self.format_bbacomm(bbacomm)
                        if inv.type == "out_invoice":
                            dups = self.search(
                                [
                                    ("id", "!=", inv.id),
                                    ("type", "=", "out_invoice"),
                                    ("state", "!=", "draft"),
                                    ("reference_type", "=", "bba"),
                                    ("reference", "=", reference),
                                ]
                            )
                            if dups:
                                partner = inv.partner_id.commercial_partner_id
                                reference = self.duplicate_bba(
                                    partner, reference
                                )
                        if reference != inv.reference:
                            vals["reference"] = reference
            super().write(vals)
        return True

    @api.returns("self", lambda value: value.id)
    def copy(self, default=None):
        self.ensure_one()
        default = default or {}
        if self.type == "out_invoice":
            reference_type = self.reference_type
            default["reference_type"] = reference_type
            if reference_type == "bba":
                partner = self.partner_id.commercial_partner_id
                default["reference"] = self.generate_bbacomm(partner)
        return super().copy(default)
