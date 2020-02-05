# -*- coding: utf-8 -*-

from StringIO import StringIO
import csv
import datetime
import itertools
import md5
from openerp import models, _

ACCOUNT = "Num\xef\xbf\xbdro de compte"
CURRENCY = "Devise"
DATE = "Date"
AMOUNT = "Montant"
BALANCE = "Solde"
COUNTERPART_NUMBER = "num\xef\xbf\xbdro de compte contrepartie"
COUNTERPART_NAME = "Nom contrepartie"
STRUCTURED_COMMUNICATION = "communication structur\xef\xbf\xbde"
FREE_COMMUNICATION = "Communication libre"
DESCRIPTION = "Description"


class CBCBankStatementImport(models.TransientModel):
    _inherit = 'account.bank.statement.import'

    _date_format = "%d/%m/%Y"

    _decimal_sep = "."
    _csv_delimiter = "\t"
    _csv_quote = '"'

    _header = ['Num\xef\xbf\xbdro de compte', 'Nom de la rubrique', 'Nom',
               'Devise', "Num\xef\xbf\xbdro de l'extrait", 'Date',
               'Description', 'Valeur', 'Montant', 'Solde',
               'cr\xef\xbf\xbddit', 'd\xef\xbf\xbdbit',
               'num\xef\xbf\xbdro de compte contrepartie', 'BIC contrepartie',
               'Nom contrepartie', 'Adresse contrepartie',
               'communication structur\xef\xbf\xbde', 'Communication libre',
               ]

    def _generate_note_cbc(self, move, communication):
        notes = []
        notes.append("%s: %s" % (_('Counter Party Name'),
                                 move[COUNTERPART_NAME].upper()))
        notes.append("%s: %s" % (_('Counter Party Account'),
                                 move[COUNTERPART_NUMBER]))
        notes.append("%s: %s" % (_('Communication'), communication))
        return '\n'.join(notes)

    def _get_move_value_cbc(self, move, sequence):
        if move[STRUCTURED_COMMUNICATION] is not None:
            communication = move[STRUCTURED_COMMUNICATION]
        else:
            communication = move[FREE_COMMUNICATION]
        move_data = {
            'name': move[DESCRIPTION],
            'note': self._generate_note_cbc(move, communication),
            'date': self._to_iso_date(move[DATE]),
            'amount': float(move[AMOUNT]),
            'account_number': move[COUNTERPART_NUMBER],
            'partner_name': move[COUNTERPART_NAME],
            'ref': (move[DATE] + '-'
                    + str(move[AMOUNT]) + '-'
                    + move[COUNTERPART_NUMBER] + '-'
                    + move[COUNTERPART_NAME]),
            'sequence': sequence,
            'unique_import_id': (move[DATE] + '-'
                                 + str(move[AMOUNT]) + '-'
                                 + str(move[BALANCE]) + '-'
                                 + move[COUNTERPART_NUMBER] + '-'
                                 + move[COUNTERPART_NAME] + '-'
                                 + md5.new(communication).hexdigest())
        }
        return move_data

    def _get_statement_data_cbc(self, balance_start, balance_end, begin_date,
                                end_date):
        statement_data = {
            'name': (_("Bank Statement from %s to %s")
                     % (begin_date, end_date)),
            'date': self._to_iso_date(end_date),
            'balance_start': balance_start,
            'balance_end_real': balance_end,
            'transactions': []
        }
        return statement_data

    def _get_acc_number_cbc(self, acc_number):
        # Check if we match the exact acc_number or the end of an acc number
        journal = self.env['account.journal'].search([
                                ('bank_acc_number', '=like', '%' + acc_number)
                                ])
        # if not found or ambiguous
        if not journal or len(journal) > 1:
            return acc_number

        return journal.bank_acc_number

    def _get_acc_balance_cbc(self, acc_number):
        if self.init_balance is not None:
            return self.init_balance

        journal = self.env['account.journal'].search([
                                ('bank_acc_number', '=like', '%' + acc_number)
                                ])
        # if not found or ambiguous
        if not journal or len(journal) > 1:
            self.init_balance = 0.0
        else:
            language = self._context.get('lang', 'en_US')
            lang = self.env['res.lang'].search([('code', '=', language)])
            bal = journal.get_journal_dashboard_datas()['last_balance'][:-1]
            self.init_balance = float(bal.strip().replace(lang.thousands_sep, '').replace(lang.decimal_point, '.')) # noqa
        return self.init_balance

    def _to_iso_date(self, orig_date):
        date_obj = datetime.datetime.strptime(orig_date, self._date_format)
        return date_obj.strftime('%Y-%m-%d')

    def _parse_file(self, data_file):

        try:
            csv_file = StringIO(data_file)
            data = csv.DictReader(csv_file, delimiter=self._csv_delimiter)
            if not data.fieldnames == self._header:
                raise ValueError()
        except ValueError:
            return super(CBCBankStatementImport, self)._parse_file(data_file)
        items = itertools.imap(lambda row: {key: item.decode('utf-8') for key, item in row.iteritems()}, data) # noqa

        currency_code = False
        account_number = False
        self.init_balance = None
        begin_date = False
        end_date = False
        balance = False

        language = self._context.get('lang', 'en_US')
        lang = self.env['res.lang'].search([('code', '=', language)])

        transactions = []
        i = 1
        sum_transaction = 0
        for statement in items:
            statement[AMOUNT] = float(statement[AMOUNT].strip().replace(lang.thousands_sep, '').replace(lang.decimal_point, '.')) # noqa
            end_date = end_date or statement[DATE]
            begin_date = statement[DATE]
            account_number = account_number or statement[ACCOUNT]
            balance = balance or self._get_acc_balance_cbc(account_number)
            currency_code = statement[CURRENCY]
            transactions.append(self._get_move_value_cbc(statement, i))
            sum_transaction += float(statement[AMOUNT])
            i += 1
        stmt = self._get_statement_data_cbc(balance, balance + sum_transaction,
                                            begin_date, end_date)
        stmt['transactions'] = transactions
        return currency_code, self._get_acc_number_cbc(account_number), [stmt]
