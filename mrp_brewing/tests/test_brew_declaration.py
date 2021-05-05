from odoo.exceptions import UserError
from odoo.fields import Date, Datetime
from odoo.tests.common import TransactionCase


class TestBrewDeclaration(TransactionCase):

    def setUp(self, *args, **kwargs):
        super(TestBrewDeclaration, self).setUp(*args, **kwargs)
        self.brew_declaration_model = self.env['brew.declaration']
        self.brew_order_model = self.env['brew.order']
        self.mrp_production_model = self.env['mrp.production']
        self.mrp_bom_model = self.env['mrp.bom']
        self.uom_unit = self.env.ref('uom.product_uom_unit')

        self.product_manuf = self.env['product.product'].create({
            'name': 'Manuf',
            'type': 'product',
            'uom_id': self.uom_unit.id,
            'is_brewable': True,
            'brew_product_sequence': self.env['ir.sequence'].create({
                    'name': 'Brew Product Sequence',
                }).id
        })

        self.product_raw_material = self.env['product.product'].create({
            'name': 'Beer Raw Material',
            'type': 'product',
            'uom_id': self.uom_unit.id,
            'raw_material': True,
        })

    def test_brew_declaration_action_cancel_draft_confirm(self):
        """Test on `brew.declaration`
        - `action_cancel`
        - `action_draft`
        - `action_confirm`
        """
        brew_declaration = self.brew_declaration_model.create({
            'request_date': Date.today()
        })
        # `draft` = default state
        self.assertEqual(brew_declaration.state, 'draft')

        # cancel it
        brew_declaration.action_cancel()
        self.assertEqual(brew_declaration.state, 'cancel')

        # change it back to draft
        brew_declaration.action_draft()
        self.assertEqual(brew_declaration.state, 'draft')

        # confirm it
        brew_declaration.action_confirm()
        self.assertEqual(brew_declaration.state, 'confirm')

    def test_brew_order_action_cancel_draft_confirm(self):
        """Test on `brew.order`
        - `action_cancel`
        - `action_draft`
        - `action_confirm`
        """
        brew_order = self.brew_order_model.create({
            'product_id': self.product_manuf.id,
            'product_qty': 100,
            'product_uom_id': self.uom_unit.id,
            'start_date': Datetime.now(),
            'wort_gathering_date': Datetime.now(),
            'end_date': Datetime.now(),
        })
        # `draft` = default state
        self.assertEqual(brew_order.state, 'draft')

        # cancel it
        brew_order.action_cancel()
        self.assertEqual(brew_order.state, 'cancel')

        # change it back to draft
        brew_order.action_draft()
        self.assertEqual(brew_order.state, 'draft')

        # confirm it without BoM
        with self.assertRaises(UserError):
            brew_order.action_confirm()

        # confirm it with BoM
        bom = self.mrp_bom_model.create({
            'product_id': self.product_manuf.id,
            'product_tmpl_id': self.product_manuf.product_tmpl_id.id,
            'bom_line_ids': ([
                (0, 0, {
                    'product_id': self.product_raw_material.id,
                    'product_qty': 1,
                    'product_uom_id': self.uom_unit.id
                }),
            ])
        })
        brew_order.action_confirm()
        self.assertEqual(brew_order.state, 'done')
        self.assertEqual(brew_order.bom.id, bom.id)
        # TODO: assert production_order_id ?
