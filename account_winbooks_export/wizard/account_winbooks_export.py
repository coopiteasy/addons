# -*- coding: utf-8 -*-
import itertools
import tempfile
from io import BytesIO
import base64

import csv
import codecs

from openerp import api, fields, models, _


class AccountUnicodeWriter(object):

    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = BytesIO()
        # created a writer with Excel formating settings
        self.writer = csv.writer(self.queue, dialect=dialect)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        # we ensure that we do not try to encode none or bool
        row = (x or u'' for x in row)

        encoded_row = [
            c.encode("utf-8") if type(c) == unicode else c for c in row]

        self.writer.writerow(encoded_row)
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        # write to the target stream
        self.stream.write(data)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


class AccountWINBOOKSExport(models.TransientModel):
    _name = 'account.winbooks.export'
    _description = 'WINBOOKS Export Accounting'

    data = fields.Binary(
        string="CSV",
        readonly=True
        )
    export_filename = fields.Char(
        string='Export CSV Filename',
        size=128,
        default='export.csv'
        )
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        readonly=True,
        default=lambda self: self.env.user.company_id
        )
    date_from = fields.Date(
        string='Start Date',
        required=True
        )
    date_to = fields.Date(
        string='End Date',
        required=True
        )

    @api.multi
    def action_manual_export_analytic_entries(self):
        self.export_filename = 'ANT.txt'
        rows = self.get_data("analytic_entries")
        with tempfile.TemporaryFile() as file_data:
            writer = AccountUnicodeWriter(file_data)
            writer.writerows(rows)
            with tempfile.TemporaryFile() as base64_data:
                file_data.seek(0)
                base64.encode(file_data, base64_data)
                base64_data.seek(0)
                self.env.cr.execute("""
                UPDATE account_winbooks_export
                SET data = %s
                WHERE id = %s""", (base64_data.read(), self.ids[0]))
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.winbooks.export',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.id,
            'views': [(False, 'form')],
            'target': 'new',
        }

    def _get_header_analytic_entries(self):
        return [
            # Standard Winbooks ANT export fields
            _(u'DBKCODE'),
            _(u'DBKTYPE'),
            _(u'DOCNUMBER'),
            _(u'BOOKYEAR'),
            _(u'PERIOD'),
            _(u'ACCOUNTGL'),
            _(u'DATE'),
            _(u'COMMENT'),
            _(u'AMOUNT'),
            _(u'AMOUNTEUR'),
            _(u'MATCHNO'),
            _(u'OLDDATE'),
            _(u'ISMATCHED'),
            _(u'ISLOCKED'),
            _(u'ISIMPORTED'),
            _(u'ISPOSITIVE'),
            _(u'SITEMP'),
            _(u'MEMOTYPE'),
            _(u'ISDOC'),
            _(u'LINEORDER'),
            _(u'AMOUNTGL'),
            _(u'DOCORDER'),
            _(u'ZONANA1'),
        ]

    def _get_rows_analytic_entries(self, date_from, date_to):
        """
        Create a generator of rows of the CSV file
        """
        self.env.cr.execute("""
        SELECT
            CASE
                WHEN account_account.code LIKE '40%%' or account_account.code LIKE '451%%' or account_account.code LIKE '70%%'
                    THEN 'VENERP'
                WHEN account_account.code LIKE '44%%' or account_account.code LIKE '411%%' or account_account.code LIKE '60%%'
                    THEN 'ACHERP'
                WHEN account_account.code LIKE '55%%'
            THEN 'BNK'
            END as DBKCODE,
            '' as DBKTYPE,
            REPLACE(SUBSTR(account_move.name, 5, 11), '/' ,'') as DOCNUMBER,
            '' as BOOKYEAR,
            '' as PERIOD,
            CASE
                WHEN account_account.code LIKE '40%%'
                    THEN '40000000'
                WHEN account_account.code LIKE '44%%'
                    THEN '44000000'
                ELSE account_account.code
            END as ACCOUNTGL,
            To_CHAR(account_move.date, 'YYYYMMDD') as DATEDOC,
            '' as DATE,
            CASE
                WHEN account_account.code LIKE '40%%'
                    THEN account_move.name
                WHEN account_account.code LIKE '44%%'
                    THEN account_move.name
                ELSE account_move_line.name
            END as COMMENT,
            '' as AMOUNT,
            round(account_move.amount,2) as AMOUNTEUR,
            '' as MATCHNO,
            '' as OLDDATE,
            '' as ISMATCHED,
            '' as ISLOCKED,
            '' as ISIMPORTED,
            '' as ISPOSITIVE,
            '' as SITEMP,
            '' as MEMOTYPE,
            '' as ISDOC,
            '' as LINEORDER,
            round(account_move.amount,2) as AMOUNTGL,
            '' as DOCORDER,
            account_analytic_account.code as ZONANA1
            FROM public.account_move_line
            JOIN account_move ON (account_move.id = account_move_line.move_id)
            JOIN account_account ON (account_account.id = account_move_line.account_id)
            JOIN account_analytic_account ON (account_analytic_account.id = account_move_line.analytic_account_id)
            WHERE (account_move.name LIKE 'FAC%%' or account_move.name LIKE 'BNK%%')
            AND (account_move.date BETWEEN %(date_from)s AND %(date_to)s)
            order by account_move_line.id
            """, {'date_from': date_from, 'date_to': date_to})

        return self.env.cr.fetchall()

    @api.multi
    def action_manual_export_partner_entries(self):
        self.export_filename = 'CSF.txt'
        rows = self.get_data("partner_entries")
        with tempfile.TemporaryFile() as file_data:
            writer = AccountUnicodeWriter(file_data)
            writer.writerows(rows)
            with tempfile.TemporaryFile() as base64_data:
                file_data.seek(0)
                base64.encode(file_data, base64_data)
                base64_data.seek(0)
                self.env.cr.execute("""
                UPDATE account_winbooks_export
                SET data = %s
                WHERE id = %s""", (base64_data.read(), self.ids[0]))
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.winbooks.export',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.id,
            'views': [(False, 'form')],
            'target': 'new',
        }

    def _get_header_partner_entries(self):
        return [
            # Standard Winbooks CSF export fields
            _(u'NUMBER'),
            _(u'TYPE'),
            _(u'NAME1'),
            _(u'NAME2'),
            _(u'CIVNAME1'),
            _(u'CIVNAME2'),
            _(u'ADRESS1'),
            _(u'ADRESS2'),
            _(u'VATCAT'),
            _(u'COUNTRY'),
            _(u'VATNUMBER'),
            _(u'PAYCODE'),
            _(u'TELNUMBER'),
            _(u'FAXNUMBER'),
            _(u'BNKACCNT'),
            _(u'ZIPCODE'),
            _(u'CITY'),
            _(u'DEFLTPOST'),
            _(u'LANG'),
            _(u'CATEGORY'),
            _(u'CENTRAL'),
            _(u'VATCODE'),
        ]

    def _get_rows_partner_entries(self, date_from, date_to):
        """
        Create a generator of rows of the CSV file
        """
        self.env.cr.execute("""
        SELECT DISTINCT
            account_account.code as NUMBER,
            CASE
                WHEN account_account.code LIKE '40%%'
                    THEN 1
                WHEN account_account.code LIKE '44%%'
                    THEN 2
            END as TYPE,
            res_partner.name as NAME1,
            res_partner.display_name as NAME2,
            '' as CIVNAME1,
            '' as CIVNAME2,
            res_partner.street as ADRESS1,
            res_partner.street2 as ADRESS2,
            CASE
                WHEN res_partner.is_company = TRUE
                    THEN 1
                ELSE 3
            END as VATCAT,
            res_country.code as COUNTRY,
            res_partner.vat as VATNUMBER,
            '' as PAYCODE,
            res_partner.phone as TELNUMBER,

            res_bank.bic as BNKACCNT,
            res_partner.zip as ZIPCODE,
            res_partner.city as CITY,
            '' as DEFLTPOST,
            res_partner.lang as LANG,
            '' as CATEGORY,
            CASE
                WHEN account_account.code LIKE '40%%'
                    THEN 40000000
                WHEN account_account.code LIKE '44%%'
                    THEN 44000000
            END as CENTRAL,
            '' as VATCODE
        FROM public.account_move_line
        JOIN account_move ON (account_move.id = account_move_line.move_id)
        JOIN account_account ON (account_account.id = account_move_line.account_id)
        JOIN res_partner ON (res_partner.id = account_move_line.partner_id)
        LEFT JOIN res_country ON (res_country.id = res_partner.country_id)
        LEFT JOIN res_partner_bank ON (res_partner_bank.partner_id = res_partner.id)
        LEFT JOIN res_bank ON (res_bank.id = res_partner_bank.bank_id)
        WHERE (account_account.code LIKE '40%%' OR account_account.code LIKE '44%%')
        AND (account_move.date BETWEEN %(date_from)s AND %(date_to)s)
        """, {'date_from': date_from, 'date_to': date_to})

        return self.env.cr.fetchall()

    @api.multi
    def action_manual_export_invoice_entries(self):
        self.export_filename = 'ACT.txt'
        rows = self.get_data("invoice_entries")
        with tempfile.TemporaryFile() as file_data:
            writer = AccountUnicodeWriter(file_data)
            writer.writerows(rows)
            with tempfile.TemporaryFile() as base64_data:
                file_data.seek(0)
                base64.encode(file_data, base64_data)
                base64_data.seek(0)
                self.env.cr.execute("""
                UPDATE account_winbooks_export
                SET data = %s
                WHERE id = %s""", (base64_data.read(), self.ids[0]))
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.winbooks.export',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.id,
            'views': [(False, 'form')],
            'target': 'new',
        }

    def _get_header_invoice_entries(self):
        return [
            # Standard Winbooks ACT export fields
            _(u'DOCTYPE'),
            _(u'DBKCODE'),
            _(u'DBKTYPE'),
            _(u'DOCNUMBER'),
            _(u'DOCORDER'),
            _(u'OPCODE'),
            _(u'ACCOUNTGL'),
            _(u'ACCOUNTRP'),
            _(u'BOOKYEAR'),
            _(u'PERIOD'),
            _(u'DATE'),
            _(u'DATEDOC'),
            _(u'DUEDATE'),
            _(u'COMMENT'),
            _(u'COMMENTEXT'),
            _(u'AMOUNT'),
            _(u'AMOUNTEUR'),
            _(u'VATBASE'),
            _(u'VATCODE'),
            _(u'VATIMPUT'),
            _(u'CURRAMOUNT'),
            _(u'CURRCODE'),
            _(u'CUREURBASE'),
            _(u'VATTAX'),
            _(u'VATIMPUT'),
            _(u'CURRATE'),
            _(u'REMINDLEV'),
            _(u'MATCHNO'),
        ]

    def _get_rows_invoice_entries(self, date_from, date_to):
        """
        Create a generator of rows of the CSV file
        """
        self.env.cr.execute("""
        SELECT
            CASE
                WHEN account_account.code LIKE '40%%'
                    THEN 1
                WHEN account_account.code LIKE '44%%'
                    THEN 2
                ELSE 3
            END as DOCTYPE,
            CASE
                WHEN (account_account.code LIKE '40%%' or account_account.code LIKE '451%%' or account_account.code LIKE '70%%') and account_move.name like 'FAC%%'
                    THEN 'VENERP'
                WHEN (account_account.code LIKE '40%%' or account_account.code LIKE '451%%' or account_account.code LIKE '70%%') and account_move.name like 'NCV%%'
                    THEN 'NCVERP'
                WHEN (account_account.code LIKE '44%%' or account_account.code LIKE '411%%' or account_account.code LIKE '604%%') and account_move.name like 'FAC%%'
                    THEN 'ACHMDS'
                WHEN (account_account.code LIKE '44%%' or account_account.code LIKE '411%%' or account_account.code LIKE '600%%') and account_move.name like 'FAC%%'
                    THEN 'ACHERP'
                WHEN (account_account.code LIKE '44%%' or account_account.code LIKE '411%%' or account_account.code LIKE '600%%') and account_move.name like 'NCA%%'
                    THEN 'NCAERP'
                WHEN (account_account.code LIKE '40%%' or account_account.code LIKE '44%%' or account_account.code LIKE '55025000') and account_move.name like 'LAV%%'
                    THEN 'LAV'
                WHEN (account_account.code LIKE '40%%' or account_account.code LIKE '44%%' or account_account.code LIKE '55%%') and account_move.name like 'BNK%%'
                    THEN 'BNK'
            END as DBKCODE,
            '' as DBKTYPE,
            REPLACE(SUBSTR(account_move.name, 5, 11), '/' ,'') as DOCNUMBER,
            '' as DOCORDER,
            '' as OPCODE,
            CASE
                WHEN account_account.code LIKE '40%%'
                    THEN '40000000'
                WHEN account_account.code LIKE '44%%'
                    THEN '44000000'
                ELSE account_account.code
            END as ACCOUNTGL,
            CASE
                WHEN account_account.code LIKE '40%%'
                    THEN account_account.code
                WHEN account_account.code LIKE '44%%'
                    THEN account_account.code
            END as ACCOUNTRP,
            '' as BOOKYEAR,
            '' as PERIOD,
            '' as DATE,
            To_CHAR(account_move.date, 'YYYYMMDD') as DATEDOC,
            '' as DUEDATE,
            CASE
            WHEN account_account.code LIKE '40%%'
                THEN account_move.name
            WHEN account_account.code LIKE '44%%'
                THEN account_move.name
            ELSE account_move_line.name
            END as COMMENT,
            account_move_line.name as COMMENTEXT,
            '' as AMOUNT,
            round(account_move_line.balance, 2) as AMOUNTEUR,
            CASE
                WHEN account_account.code LIKE '40%%' or account_account.code LIKE '44%%'
                    THEN round(account_move.amount / 1.21, 2)
                WHEN account_account.code LIKE '451%%' or account_account.code LIKE '411%%'
                    THEN round(account_move.amount / 1.21, 2)
            END as VATBASE,
            CASE
                WHEN account_account.code LIKE '451%%'
                    THEN round(account_tax.amount)
                WHEN account_account.code LIKE '411%%'
                    THEN round(account_tax.amount)
            END as VATCODE,
            '' as CURRAMOUNT,
            '' as CURRCODE,
            '' as CUREURBASE,
            '' as VATTAX,
            '' as VATIMPUT,
            '' as CURRATE,
            '' as REMINDLEV,
            account_full_reconcile.name as MATCHNO
        FROM public.account_move_line
        JOIN account_move ON (account_move.id = account_move_line.move_id)
        JOIN account_account ON (account_account.id = account_move_line.account_id)
        LEFT JOIN account_full_reconcile ON (account_full_reconcile.id = account_move_line.full_reconcile_id)
        LEFT JOIN account_tax ON (account_tax.id = account_move_line.tax_line_id)
        WHERE (account_move.name LIKE 'FAC%%' or account_move.name LIKE 'BNK%%' or account_move.name LIKE 'NC%%')
        AND (account_move.date BETWEEN %(date_from)s AND %(date_to)s)
        order by account_move_line.id, doctype
        """, {'date_from': date_from, 'date_to': date_to})

        return self.env.cr.fetchall()

    def get_data(self, result_type):
        data = {}
        get_rows_func = getattr(self, ("_get_rows_%s" % (result_type)))

        data['form'] = self.read(['date_from', 'date_to'])[0]
        date_from = data['form']['date_from']
        date_to = data['form']['date_to']

        rows = itertools.chain(get_rows_func(date_from, date_to))
        return rows
