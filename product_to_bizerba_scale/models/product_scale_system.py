# Copyright 2014-2017 GRAP (http://www.grap.coop)
#   - Sylvain LE GAL (https://twitter.com/legalsylvain)
# Copyright 2017-Today Coop IT Easy SC
#   - Houssine BAKKALI <houssine@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ProductScaleSystem(models.Model):
    _name = "product.scale.system"
    _description = "Product Scale System"

    # Constant section
    _ENCODING_SELECTION = [
        ("iso-8859-1", "Latin 1 (iso-8859-1)"),
        ("cp1252", "Latin 1 (cp1252)"),
        ("utf-8", "UTF-8"),
    ]

    def _compute_field_ids(self):
        for system in self:
            values = []
            for product_line in system.product_line_ids:
                if product_line.field_id:
                    values.append(product_line.field_id.id)
            system.field_ids = values

    name = fields.Char(string="Name", required=True)
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        default=lambda self: self.env["res.company"]._company_default_get(
            "product.template"
        ),
        index=True,
    )
    active = fields.Boolean(string="Active", default=True)
    ftp_url = fields.Char(string="FTP Server URL", default="xxx.xxx.xxx.xxx")
    ftp_login = fields.Char(string="FTP Login")
    ftp_password = fields.Char(string="FTP Password")
    encoding = fields.Selection(
        selection=_ENCODING_SELECTION,
        string="Encoding",
        default="iso-8859-1",
        required=True,
    )
    csv_relative_path = fields.Char(
        string="Relative Path for CSV", default="/", required=True
    )
    product_image_relative_path = fields.Char(
        string="Relative Path for Product Images", default="/", required=True
    )
    product_text_file_pattern = fields.Char(
        string="Product Text File Pattern",
        required=True,
        default="product.csv",
        help="Pattern of the Product file. Use % to include dated information. "
        "Ref: https://docs.python.org/2/library/time.html#time.strftime",
    )
    external_text_file_pattern = fields.Char(
        string="External Text File Pattern",
        required=True,
        default="external_text.csv",
        help="Pattern of the External Text file. Use % to include dated "
        "information. "
        "Ref: https://docs.python.org/2/library/time.html#time.strftime",
    )
    product_line_ids = fields.One2many(
        comodel_name="product.scale.system.product.line",
        inverse_name="scale_system_id",
        string="Product Lines",
    )
    field_ids = fields.One2many(
        comodel_name="ir.model.fields",
        compute="_compute_field_ids",
        string="Fields",
    )
