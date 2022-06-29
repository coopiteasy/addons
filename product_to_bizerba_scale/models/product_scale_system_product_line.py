# Copyright 2014-2017 GRAP (http://www.grap.coop)
#   - Sylvain LE GAL (https://twitter.com/legalsylvain)
# Copyright 2017-Today Coop IT Easy SC
#   - Houssine BAKKALI <houssine@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductScaleSystemProductLine(models.Model):
    _name = "product.scale.system.product.line"
    _description = "Product Scale System Product Line"
    _order = "scale_system_id, sequence"

    _TYPE_SELECTION = [
        ("id", "Product ID"),
        ("numeric", "Numeric Field"),
        ("text", "Char / Text Field"),
        ("external_text", "External Text Field"),
        ("constant", "Constant Value"),
        ("external_constant", "External Constant Text Value"),
        ("many2one", "Many2One Field"),
        ("many2many", "Many2Many Field"),
        ("product_image", "Product Image"),
    ]

    scale_system_id = fields.Many2one(
        comodel_name="product.scale.system",
        inverse_name="Scale System",
        required=True,
        ondelete="cascade",
        index=True,
    )
    company_id = fields.Many2one(
        related="scale_system_id.company_id", string="Company", store=True
    )
    code = fields.Char(string="Bizerba Code", required=True)
    name = fields.Char(string="Name", required=True)
    sequence = fields.Integer(string="Sequence", required=True, default=10)
    type = fields.Selection(selection=_TYPE_SELECTION, string="Type")
    field_id = fields.Many2one(
        comodel_name="ir.model.fields",
        string="Product Field",
        domain="[('model', 'in', ['product.template'])]",
    )

    # TODO Improve. Set domain, depending on the other field
    related_field_id = fields.Many2one(
        comodel_name="ir.model.fields",
        string="M2M / M2O Field",
        help="Used only for the x2x fields. Set here the field of the related "
        "model that you want to send to the "
        "scale. Let empty to send the ID. ",
    )

    x2many_range = fields.Integer(
        string="range of the x2Many Fields",
        help="Used if type is 'Many2Many Field', to mention the range of the "
        "field  to send. Begin by 0. (used for "
        "exemple for product logos) ",
    )
    constant_value = fields.Char(
        string="Constant Value",
        help="Used if type is 'constant', to always send the same value.",
    )
    multiline_length = fields.Integer(
        string="Length for Multiline",
        help="Used if type is 'Text Field' or 'External Text Constant', "
        "to indicate the max length of a line. Set 0 "
        "to avoid to split the value.",
        default=0,
    )
    multiline_separator = fields.Char(
        string="Separator for Multiline",
        help="Used if type is 'Text Field' or 'External Text Constant', "
        "to indicate wich text will be used to mention "
        "break lines.",
        default="\n",
    )

    # TODO Improve. Set contrains.
    suffix = fields.Char(
        string="Suffix",
        help="Used if type is 'External Text Field', to indicate how to "
        "suffix the field.\nMake sure to have a uniq "
        "value by Scale System, and all with the same size.\n\nUsed if type "
        "is Product Image to mention the end "
        "of the file. Exemple : '_01.jpg'. ",
    )
    numeric_coefficient = fields.Float(
        string="Numeric Coefficient",
        help="Used if type is 'Numeric Field', to mention which coefficient "
        "numeric field should be multiplied.",
        default=1,
    )

    numeric_round = fields.Float(
        string="Rounding Method",
        help="Used if type is 'Numeric Field', to mention how the value "
        "should be rounded.\nDo not Use 0, because it "
        "will truncate the value.",
        default=1,
    )
    delimiter = fields.Char(
        string="Delimiter Char", help="Used to finish the column", default="#"
    )
