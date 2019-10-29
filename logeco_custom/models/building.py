from odoo import fields, models


class Building(models.Model):
    _inherit = "hc.building"

    country_id = fields.Many2one(default=43)

    surface_hm = fields.Integer(string="Surface HM", required=False, help="m²")
    housings_hm = fields.Integer(
        string="Number of HM housings", required=False
    )

    surface_lup = fields.Integer(
        string="Surface LUP", required=False, help="m²"
    )
    housings_lup = fields.Integer(
        string="Number of LUP housings", required=False
    )

    surface_zdloc = fields.Integer(
        string="Surface ZDLOC", required=False, help="m²"
    )
    housings_zdloc = fields.Integer(
        string="Number of ZDLOC housings", required=False
    )

    ddp_start = fields.Date(
        string="Start of 'droit distinct et permanent' (DDP)", required=False
    )
    ddp_duration = fields.Integer(
        string="Duration of 'droit distinct et permanent' (DDP)",
        required=False,
        help="Years",
    )
    lgl_end = fields.Date(string="End of 'LGL' benefits", required=False)
