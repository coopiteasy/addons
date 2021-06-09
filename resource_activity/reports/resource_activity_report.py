# -*- coding: utf-8 -*-


from openerp import tools
from openerp import models, fields


class ResourceActivityReport(models.Model):
    _name = "resource.activity.report"
    _description = "Activities Analysis"
    _auto = False

    activity_theme = fields.Many2one(
        comodel_name="resource.activity.theme",
        string="Activity Theme",
        readonly=True,
    )
    activity_type = fields.Many2one(
        comodel_name="resource.activity.type",
        string="Activity Type",
        readonly=True,
    )
    analytic_account = fields.Many2one(
        comodel_name="account.analytic.account",
        string="Analytic Account",
        readonly=True,
    )
    attendee_category_id = fields.Many2one(
        comodel_name="res.partner.category",
        string="Attendee Category",
        readonly=True,
    )
    booked_resource_id = fields.Many2one(
        comodel_name="resource.resource",
        string="Booked Resource",
        readonly=True,
    )
    booked_resource_state = fields.Selection(
        [
            ("draft", "Draft"),
            ("available", "Available"),
            ("unavailable", "Unavailable"),
        ],
        string="Booked Resource State",
        readonly=True,
    )
    date_start = fields.Datetime(string="Date Start", readonly=True)
    duration = fields.Char(string="Duration", readonly=True)
    lang_id = fields.Many2one(
        comodel_name="resource.activity.lang", string="Language", readonly=True
    )
    location_id = fields.Many2one(
        comodel_name="resource.location", string="Location", readonly=True
    )
    nb_allocated_resources = fields.Integer(
        string="Allocated Resources", readonly=True
    )
    need_delivery = fields.Boolean(string="Need Delivery?", readonly=True)
    need_guide = fields.Boolean(string="Need Guide?", readonly=True)
    product_id = fields.Many2one(
        comodel_name="product.product", string="Product", readonly=True
    )
    product_categ_id = fields.Many2one(
        comodel_name="product.category",
        string="Product Category",
        readonly=True,
    )
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("quotation", "Quotation"),
            ("sale", "Sale"),
            ("done", "Done"),
            ("cancelled", "Cancelled"),
        ],
        string="Status",
        readonly=True,
    )
    total_participants = fields.Integer(
        string="Total Participants", readonly=True,
    )
    total_participants_with_resource = fields.Integer(
        string="Total Participants w/ resource", readonly=True,
    )
    total_participants_without_resource = fields.Integer(
        string="Total Participants w/o resource", readonly=True,
    )
    total_quantity_allocated = fields.Float(
        "Total Quantity Allocated", readonly=True
    )
    total_renting_days = fields.Integer("Total Renting Days", readonly=True)
    total_renting_hours = fields.Float("Total Renting Hours", readonly=True)
    total_taxed_amount = fields.Float("Total Amount incl. tax", readonly=True)
    total_untaxed_amount = fields.Float(
        "Total Amount excl. tax", readonly=True
    )

    def _activities_as(self):
        as_str = """
            %s
            %s
        """ % (
            self._select_activities(),
            self._from_activities(),
        )
        return as_str

    def _select_activities(self):
        select_str = """
            SELECT ra.id AS activity_id,
                   ra.activity_theme,
                   ra.activity_type,
                   ra.date_end,
                   ra.date_start,
                   rat.analytic_account,
                   ra.location_id,
                   ra.nb_allocated_resources,
                   ra.need_delivery,
                   ra.need_guide,
                   ra.state,
                   ra.sale_order_id,
                   ra.registrations_expected AS total_participants,
                   ra.registrations_expected - ra.without_resource_reg AS total_participants_with_resource,
                   ra.without_resource_reg AS total_participants_without_resource
        """
        return select_str

    def _from_activities(self):
        from_str = """
            FROM resource_activity ra
                 JOIN resource_activity_type rat ON ra.activity_type = rat.id
        """
        return from_str

    def _attendee_categories_as(self):
        as_str = """
            %s
            %s
            %s
            %s
        """ % (
            self._select_attendee_categories(),
            self._from_attendee_categories(),
            self._group_by_attendee_categories(),
            self._order_by_attendee_categories(),
        )
        return as_str

    def _select_attendee_categories(self):
        select_str = """
            SELECT ra.id AS activity_id,
                   rprpcr.category_id as attendee_category_id
        """
        return select_str

    def _from_attendee_categories(self):
        from_str = """
            FROM resource_activity ra
                 JOIN resource_activity_registration rar ON ra.id = rar.resource_activity_id
                 JOIN res_partner rp on rar.attendee_id = rp.id
                 JOIN res_partner_res_partner_category_rel rprpcr on rp.id = rprpcr.partner_id
        """
        return from_str

    def _group_by_attendee_categories(self):
        group_by_str = """
            GROUP BY ra.id,
                     rp.id,
                     rprpcr.category_id
        """
        return group_by_str

    def _order_by_attendee_categories(self):
        order_by_str = """
            ORDER BY ra.id,
                     rp.id,
                     rprpcr.category_id
        """
        return order_by_str

    def _booked_resources_as(self):
        as_str = """
            %s
            %s
            %s
            %s
            %s
        """ % (
            self._select_booked_resources(),
            self._from_booked_resources(),
            self._where_booked_resources(),
            self._group_by_booked_resources(),
            self._order_by_booked_resources(),
        )
        return as_str

    def _select_booked_resources(self):
        select_str = """
            SELECT ra.id AS activity_id,
                   rar.id as registration_id,
                   r.resource_id as booked_resource_id,
                   r.state as booked_resource_state
            """
        return select_str

    def _from_booked_resources(self):
        from_str = """
            FROM resource_activity ra
                 JOIN resource_activity_registration rar ON ra.id = rar.resource_activity_id
                 JOIN resource_allocation r on rar.id = r.activity_registration_id
        """
        return from_str

    def _where_booked_resources(self):
        where_str = """
            WHERE r.state IN ('option', 'booked')
        """
        return where_str

    def _group_by_booked_resources(self):
        group_by_str = """
            GROUP BY ra.id, 
                     rar.id, 
                     r.resource_id, 
                     r.state
        """
        return group_by_str

    def _order_by_booked_resources(self):
        order_by_str = """
            ORDER BY ra.id
        """
        return order_by_str

    def _languages_as(self):
        as_str = """
            %s
            %s
        """ % (
            self._select_languages(),
            self._from_languages(),
        )
        return as_str

    def _select_languages(self):
        select_str = """
            SELECT ra.id AS activity_id,
                   ral.id AS lang_id
        """
        return select_str

    def _from_languages(self):
        from_str = """
            FROM resource_activity ra
                 JOIN resource_activity_resource_activity_lang_rel raralr ON ra.id = raralr.resource_activity_id
                 JOIN resource_activity_lang ral ON ral.id = raralr.resource_activity_lang_id
        """
        return from_str

    def _products_as(self):
        as_str = """
            %s
            %s
            %s
            %s
        """ % (
            self._select_products(),
            self._from_products(),
            self._group_by_products(),
            self._order_by_products(),
        )
        return as_str

    def _select_products(self):
        select_str = """
            SELECT ra.id AS activity_id,
                   pp.id AS product_id,
                   pt.categ_id AS product_categ_id
            """
        return select_str

    def _from_products(self):
        from_str = """
            FROM resource_activity ra
                 JOIN resource_activity_registration rar ON ra.id = rar.resource_activity_id
                 JOIN product_product pp ON rar.product_id = pp.id
                 JOIN product_template pt ON pp.product_tmpl_id = pt.id
        """
        return from_str

    def _group_by_products(self):
        group_by_str = """
            GROUP BY ra.id,
                     pp.id,
                     pt.categ_id
        """
        return group_by_str

    def _order_by_products(self):
        order_by_str = """
            ORDER BY ra.id
        """
        return order_by_str

    def _sale_orders_as(self):
        as_str = """
            %s
            %s
            %s
        """ % (
            self._select_sale_orders(),
            self._from_sale_orders(),
            self._group_by_sale_orders(),
        )
        return as_str

    def _select_sale_orders(self):
        select_str = """
            SELECT ra.id AS activity_id,
                   sum(so.amount_total) AS total_taxed_amount,
                   sum(so.amount_untaxed) AS total_untaxed_amount
        """
        return select_str

    def _from_sale_orders(self):
        from_str = """
            FROM resource_activity ra
                 JOIN sale_order so ON ra.id = so.activity_id
        """
        return from_str

    def _group_by_sale_orders(self):
        group_by_str = """
            GROUP BY ra.id
        """
        return group_by_str

    def _registrations_as(self):
        as_str = """
            %s
            %s
            %s
            %s
        """ % (
            self._select_registrations(),
            self._from_registrations(),
            self._group_by_registrations(),
            self._order_by_registrations(),
        )
        return as_str

    def _select_registrations(self):
        select_str = """
            SELECT ra.id AS activity_id,
                   sum(rar.quantity_allocated) AS total_quantity_allocated,
                   sum(rar.quantity_allocated) * extract(epoch FROM ra.date_end - ra.date_start) / 3600 AS total_renting_hours,
                   sum(rar.quantity_allocated) * extract(epoch FROM ra.date_end - ra.date_start) / 3600 / 24 AS total_renting_days
        """
        return select_str

    def _from_registrations(self):
        from_str = """
            FROM resource_activity ra
                 JOIN resource_activity_registration rar ON ra.id = rar.resource_activity_id
        """
        return from_str

    def _group_by_registrations(self):
        group_by_str = """
            GROUP BY ra.id
        """
        return group_by_str

    def _order_by_registrations(self):
        order_by_str = """
            ORDER BY ra.id
        """
        return order_by_str

    def _select(self):
        select_str = """
            SELECT a.activity_id AS id,
                   a.activity_theme,
                   a.activity_type,
                   a.date_end,
                   a.date_start,
                   a.analytic_account,
                   a.location_id,
                   a.nb_allocated_resources,
                   a.need_delivery,
                   a.need_guide,
                   a.state,
                   a.sale_order_id,
                   a.total_participants,
                   a.total_participants_with_resource,
                   a.total_participants_without_resource,
                   ac.attendee_category_id,
                   br.booked_resource_id,
                   br.booked_resource_state,
                   l.lang_id,
                   p.product_categ_id,
                   p.product_id,
                   so.total_taxed_amount,
                   so.total_untaxed_amount,
                   total_quantity_allocated,
                   total_renting_hours,
                   total_renting_days
        """
        return select_str

    def _from(self):
        from_str = """
            FROM activities a
                 LEFT JOIN attendee_categories ac ON ac.activity_id = a.activity_id
                 LEFT JOIN booked_resources br ON br.activity_id = a.activity_id
                 LEFT JOIN languages l ON l.activity_id = a.activity_id 
                 LEFT JOIN products p ON p.activity_id = a.activity_id
                 LEFT JOIN sale_orders so ON so.activity_id = a.activity_id
                 LEFT JOIN registrations r ON r.activity_id = a.activity_id
        """
        return from_str

    def _where(self):
        where_str = """"""
        return where_str

    def _group_by(self):
        group_by_str = """"""
        return group_by_str

    def _order_by(self):
        order_by_str = """
            ORDER BY a.activity_id
        """
        return order_by_str

    def init(self, cr):
        tools.drop_view_if_exists(cr, self._table)
        cr.execute(
            """
            CREATE or REPLACE VIEW %s as (
                WITH 
                    activities AS (%s),
                    attendee_categories AS (%s),
                    booked_resources AS (%s),
                    languages AS (%s),
                    products AS (%s),
                    sale_orders AS (%s),
                    registrations AS (%s)
                    %s
                    %s
                    %s
                    %s
                    %s
            )"""
            % (
                self._table,
                self._activities_as(),
                self._attendee_categories_as(),
                self._booked_resources_as(),
                self._languages_as(),
                self._products_as(),
                self._sale_orders_as(),
                self._registrations_as(),
                self._select(),
                self._from(),
                self._where(),
                self._group_by(),
                self._order_by(),
            )
        )
