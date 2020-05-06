# Copyright 2020 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.multi
    def generate_ref_code(self, prefix, sequence):
        for product in self:
            number = sequence.next_by_id()
            code = prefix + number

            while self.search([("default_code", "=", code)]) and number < 1000:
                number = sequence.next_by_id()
                code = prefix + number

            if number == 1000:
                _logger.error(
                    "maximum inscrementation number (1000) reached for sequence %s."
                    " It needs to be reset."
                )
                raise ValidationError(
                    _(
                        "You have reached the limit for default code generation."
                        " Please contact your system administrator.\n\n"
                        "%s" % sequence
                    )
                )

            product.default_code = code
        self.generate_barcode()

    @api.multi
    def generate_ref_code_pp(self):
        sequence = self.env.ref(
            "spp_custom.seq_ean_product_internal_ref_weight_pp"
        )
        self.generate_ref_code("01", sequence)

    @api.multi
    def generate_ref_code_bio_producer(self):
        sequence = self.env.ref(
            "spp_custom.seq_ean_product_internal_ref_weight_bio_producer"
        )
        self.generate_ref_code("02", sequence)

    @api.multi
    def generate_ref_code_bio_supplier(self):
        sequence = self.env.ref(
            "spp_custom.seq_ean_product_internal_ref_weight_bio_supplier"
        )
        self.generate_ref_code("03", sequence)

    @api.multi
    def generate_ref_code_non_bio(self):
        sequence = self.env.ref(
            "spp_custom.seq_ean_product_internal_ref_weight_non_bio"
        )
        self.generate_ref_code("09", sequence)
