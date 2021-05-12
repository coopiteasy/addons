from odoo import api, models


class IrModelData(models.TransientModel):
    _name = 'auto.reload.banks.module'

    @api.model
    def import_bank_data(self):
        bank_data_wizard = self.sudo().env["l10n.es.partner.import.wizard"].create({})
        bank_data_wizard.execute()

