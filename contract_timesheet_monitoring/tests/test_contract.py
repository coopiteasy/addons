from odoo.addons.hr_timesheet.tests.test_timesheet import TestCommonTimesheet


class TestContractTimeSpent(TestCommonTimesheet):
    @classmethod
    def setUpClass(cls):
        super(TestContractTimeSpent, cls).setUpClass()

        cls.contract = cls.env["contract.contract"].create(
            {
                "name": "Test Contract Service",
                "partner_id": cls.partner.id,
                # "pricelist_id": cls.partner.property_product_pricelist.id,
                # "line_recurrence": True,
                # "contract_type": "purchase",
                "contract_line_ids": [
                    (
                        0,
                        0,
                        {
                            # "product_id": cls.product_1.id,
                            "name": "Services from #START# to #END#",
                            "analytic_distribution": {cls.analytic_account.id: 100},
                            "quantity": 1,
                            "uom_id": cls.env.ref("uom.product_uom_hour").id,
                            "price_unit": 100,
                            "recurring_rule_type": "monthly",
                            "recurring_interval": 1,
                            "date_start": "2024-01-01",
                            "recurring_next_date": "2024-12-31",
                        },
                    )
                ],
            }
        )
        cls.env["account.analytic.line"].create(
            {
                "project_id": cls.project_customer.id,
                "task_id": cls.task1.id,
                "name": "timesheet1",
                "unit_amount": 1,
                "date": "2024-02-01",
                "employee_id": cls.empl_employee2.id,
            }
        )
        cls.env["account.analytic.line"].create(
            {
                "project_id": cls.project_customer.id,
                "task_id": cls.task1.id,
                "name": "timesheet2",
                "unit_amount": 1,
                "date": "2023-02-01",
                "employee_id": cls.empl_employee2.id,
            }
        )

    def test_time_spent_in_period(self):
        self.assertEqual(self.contract.contract_line_ids[0].time_spent, 1)
