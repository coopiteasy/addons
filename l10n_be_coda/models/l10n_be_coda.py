# -*- encoding: utf-8 -*-
##############################################################################
#
#    UNamur - University of Namur, Belgium (www.unamur.be)
#    Noviat nv/sa (www.noviat.be)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
import time

from openerp import models, fields, _
from openerp.exceptions import ValidationError
from openerp import tools
from openerp.addons.base.res.res_bank import sanitize_account_number

import logging

_logger = logging.getLogger(__name__)


def rmspaces(s):
    return " ".join(s.split())


class CodaImport:

    def _parse_line(self, line, statements):
        if not line:
            return
        if line[0] == '0':
            statement = {}
            statements.append(statement)
        else:
            statement = statements[-1]
        try:
            meth = getattr(self, '_parse_line_%s' % line[0])
        except:
            raise ValidationError(_("CODA parsing error: lines starting with '%s' are not supported") % line[0])
        meth(line, statement)

    def _parse_line_0(self, line, statement):
        # Begin of a new Bank statement
        statement['version'] = line[127]
        if statement['version'] not in ['1', '2']:
            raise ValidationError(_('Error R001: CODA V%s statements are not supported, please '
                                    'contact your bank') % statement['version'])
        statement['globalisation_stack'] = []
        statement['lines'] = []
        statement['date'] = time.strftime(tools.DEFAULT_SERVER_DATE_FORMAT,
                                          time.strptime(rmspaces(line[5:11]), '%d%m%y'))
        statement['separateApplication'] = rmspaces(line[83:88])

    def _parse_line_1(self, line, statement):
        # Statement details
        if statement['version'] == '1':
            statement['acc_number'] = sanitize_account_number(line[5:17])
            statement['currency'] = rmspaces(line[18:21])
        elif statement['version'] == '2':
            if line[1] == '0':  # Belgian bank account BBAN structure
                statement['acc_number'] = sanitize_account_number(line[5:17])
                statement['currency'] = rmspaces(line[18:21])
            elif line[1] == '1':  # foreign bank account BBAN structure
                raise ValidationError(_('Error R1001: Foreign bank accounts with BBAN '
                                        'structure are not supported'))
            elif line[1] == '2':    # Belgian bank account IBAN structure
                statement['acc_number'] = sanitize_account_number(line[5:21])
                statement['currency'] = rmspaces(line[39:42])
            elif line[1] == '3':    # foreign bank account IBAN structure
                raise ValidationError(_('Error R1002: Foreign bank accounts with IBAN structure '
                                        'are not supported'))
            else:  # Something else, not supported
                raise ValidationError(_('Error R1003: Unsupported bank account structure'))
        statement['description'] = rmspaces(line[90:125])
        statement['balance_start'] = float(rmspaces(line[43:58])) / 1000
        if line[42] == '1':  # 1 = Debit, the starting balance is negative
            statement['balance_start'] = - statement['balance_start']
        statement['balance_start_date'] = time.strftime(tools.DEFAULT_SERVER_DATE_FORMAT,
                                                        time.strptime(rmspaces(line[58:64]), '%d%m%y'))
        statement['accountHolder'] = rmspaces(line[64:90])
        statement['paperSeqNumber'] = rmspaces(line[2:5])
        statement['codaSeqNumber'] = rmspaces(line[125:128])

    def _parse_line_2(self, line, statement):
        if line[1] == '1':
            self._parse_line_21(line, statement)
        elif line[1] == '2':
            self._parse_line_22(line, statement)
        elif line[1] == '3':
            self._parse_line_23(line, statement)
        else:
            # movement data record 2.x (x != 1,2,3)
            raise ValidationError(_('Movement data records of type 2.%s are not supported') % line[1])

    def _parse_line_21(self, line, statement):
        # New statement line
        st_line = {}
        prev_line = False
        st_line['ref'] = rmspaces(line[2:10])
        st_line['ref_move'] = rmspaces(line[2:6])
        st_line['ref_move_detail'] = rmspaces(line[6:10])
        if int(line[6:10]) > 0:
            prev_line = statement['lines'][-1]
        st_line['sequence'] = len(statement['lines']) + 1
        st_line['transactionRef'] = rmspaces(line[10:31])
        st_line['debit'] = line[31]  # 0 = Credit, 1 = Debit
        st_line['amount'] = float(rmspaces(line[32:47])) / 1000
        if st_line['debit'] == '1':
            st_line['amount'] = - st_line['amount']
        st_line['transactionDate'] = time.strftime(tools.DEFAULT_SERVER_DATE_FORMAT,
                                                   time.strptime(rmspaces(line[47:53]), '%d%m%y'))
        st_line['transaction_family'] = rmspaces(line[54:56])
        st_line['transaction_code'] = rmspaces(line[56:58])
        st_line['transaction_category'] = rmspaces(line[58:61])
        if line[61] == '1':
            # Structured communication
            st_line['communication_struct'] = True
            st_line['communication_type'] = line[62:65]
            st_line['communication'] = ('+++' + line[65:68] + '/' + line[68:72] + '/' + line[72:77] + '+++')
        else:
            # Non-structured communication
            st_line['communication_struct'] = False
            st_line['communication'] = rmspaces(line[62:115])

        if not(st_line['communication']) and prev_line:
            st_line['communication'] = prev_line['communication']
            if st_line['communication_struct'] and not(st_line.get('communication_type')):
                st_line['communication_type'] = prev_line['communication_type']

        st_line['entryDate'] = time.strftime(
            tools.DEFAULT_SERVER_DATE_FORMAT, time.strptime(rmspaces(line[115:121]), '%d%m%y'))
        st_line['type'] = 'normal'
        st_line['extract_number'] = rmspaces(line[122:124])
        st_line['globalisation'] = int(line[124])
        if st_line['globalisation'] > 0:
            if st_line['globalisation'] in statement['globalisation_stack']:
                statement['globalisation_stack'].remove(st_line['globalisation'])
            else:
                st_line['type'] = 'globalisation'
                statement['globalisation_stack'].append(st_line['globalisation'])
            self.global_comm[st_line['ref_move']] = st_line['communication']
        if not st_line.get('communication'):
            st_line['communication'] = self.global_comm.get(st_line['ref_move'], '')
        statement['lines'].append(st_line)

    def _parse_line_22(self, line, statement):
        if statement['lines'][-1]['ref'][0:4] != line[2:6]:
            raise ValidationError(_('CODA parsing error on movement data record 2.2, seq nr %s! '
                                    'Please report this issue via your Odoo support channel.') % line[2:10])
        statement['lines'][-1]['communication'] += rmspaces(line[10:63])
        statement['lines'][-1]['payment_reference'] = rmspaces(line[63:98])
        statement['lines'][-1]['counterparty_bic'] = rmspaces(line[98:109])

    def _parse_line_23(self, line, statement):
        if statement['lines'][-1]['ref'][0:4] != line[2:6]:
            raise ValidationError(_('CODA parsing error on movement data record 2.3, seq nr %s!'
                                    'Please report this issue via your Odoo support channel.') % line[2:10])
        if statement['version'] == '1':
            statement['lines'][-1]['counterpartyNumber'] = sanitize_account_number(line[10:22])
            statement['lines'][-1]['counterpartyName'] = rmspaces(line[47:73])
            statement['lines'][-1]['counterpartyAddress'] = rmspaces(line[73:125])
            statement['lines'][-1]['counterpartyCurrency'] = ''
        else:
            if line[22] == ' ':
                statement['lines'][-1]['counterpartyNumber'] = sanitize_account_number(line[10:22])
                statement['lines'][-1]['counterpartyCurrency'] = rmspaces(line[23:26])
            else:
                statement['lines'][-1]['counterpartyNumber'] = sanitize_account_number(line[10:44])
                statement['lines'][-1]['counterpartyCurrency'] = rmspaces(line[44:47])
            statement['lines'][-1]['counterpartyName'] = rmspaces(line[47:82])
            statement['lines'][-1]['communication'] += rmspaces(line[82:125])

    def _parse_line_3(self, line, statement):
        if line[1] == '1':
            infoLine = {}
            infoLine['entryDate'] = statement['lines'][-1]['entryDate']
            infoLine['type'] = 'information'
            infoLine['sequence'] = len(statement['lines']) + 1
            infoLine['ref'] = rmspaces(line[2:10])
            infoLine['transactionRef'] = rmspaces(line[10:31])
            infoLine['transaction_family'] = rmspaces(line[32:34])
            infoLine['transaction_code'] = rmspaces(line[34:36])
            infoLine['transaction_category'] = rmspaces(line[36:39])
            infoLine['communication'] = rmspaces(line[40:113])
            statement['lines'].append(infoLine)
        elif line[1] == '2':
            infoLine = statement['lines'][-1]
            if infoLine['ref'] != rmspaces(line[2:10]):
                raise ValidationError(_('CODA parsing error on information data record 3.2, seq nr %s! '
                                        'Please report this issue via your Odoo support channel.') % line[2:10])
            statement['lines'][-1]['communication'] += rmspaces(line[10:100])
        elif line[1] == '3':
            infoLine = statement['lines'][-1]
            if infoLine['ref'] != rmspaces(line[2:10]):
                raise ValidationError(_('CODA parsing error on information data record 3.3, seq nr %s! '
                                        'Please report this issue via your Odoo support channel.') % line[2:10])
            statement['lines'][-1]['communication'] += rmspaces(line[10:100])

    def _parse_line_4(self, line, statement):
        comm_line = {}
        comm_line['type'] = 'communication'
        comm_line['sequence'] = len(statement['lines']) + 1
        comm_line['ref'] = rmspaces(line[2:10])
        comm_line['communication'] = rmspaces(line[32:112])
        statement['lines'].append(comm_line)

    def _parse_line_8(self, line, statement):
        # new balance record
        statement['debit'] = line[41]
        statement['paperSeqNumber'] = rmspaces(line[1:4])
        statement['balance_end_real'] = float(rmspaces(line[42:57])) / 1000
        statement['date'] = time.strftime(tools.DEFAULT_SERVER_DATE_FORMAT,
                                          time.strptime(rmspaces(line[57:63]), '%d%m%y'))
        if statement['debit'] == '1':    # 1=Debit
            statement['balance_end_real'] = - statement['balance_end_real']

    def _parse_line_9(self, line, statement):
        statement['balanceMin'] = float(rmspaces(line[22:37])) / 1000
        statement['balancePlus'] = float(rmspaces(line[37:52])) / 1000
        if not statement.get('balance_end_real'):
            statement['balance_end_real'] = statement['balance_start'] + \
                statement['balancePlus'] - statement['balanceMin']

    def _get_transactions(self, coda_statement):
        transactions = []
        for line in coda_statement['lines']:
            transaction = {}
            if line['type'] == 'information':
                coda_statement['coda_note'] = "\n".join([coda_statement['coda_note'],
                                                         line['type'].title() + ' with Ref. ' + str(line['ref']),
                                                         'Date: ' + str(line['entryDate']),
                                                         'Communication: ' + line['communication'], ''])
            elif line['type'] == 'communication':
                coda_statement['coda_note'] = "\n".join([coda_statement['coda_note'],
                                                         line['type'].title() + ' with Ref. ' + str(line['ref']),
                                                         'Ref: ', 'Communication: ' + line['communication'], ''])
            elif line['type'] == 'normal':
                note = []
                extract_number = ''
                if 'counterpartyAddress' in line and line['counterpartyAddress'] != '':
                    note.append(_('Counter Party Address') + ': ' + line['counterpartyAddress'])
                structured_com = False
                if line['communication_struct'] and line.get('communication_type') == '101':
                    structured_com = line['communication']
                if line.get('counterpartyName'):
                    note.append(_('Counter Party') + ': ' + line['counterpartyName'])
                    transaction['partner_name'] = line['counterpartyName']
                if line.get('counterpartyNumber'):
                    note.append(_('Counter Party Account') + ': ' + line['counterpartyNumber'])
                    transaction['account_number'] = line['counterpartyNumber']
                if line.get('communication'):
                    note.append(_('Communication') + ': ' + line['communication'])
                if line['extract_number']:
                    extract_number = line['extract_number']
                transaction.update({
                    'name': structured_com or (line.get('communication', '') != '' and line['communication'] or '/'),
                    'date': line['entryDate'],
                    'amount': line['amount'],
                    'unique_import_id': line['counterpartyNumber'] + '-' + line.get('communication', '') + '-' + line['entryDate'] + '-' + line['entryDate'] + '-' +  line['ref'],
                    'note': "\n".join(note),
                    'ref': line['ref'],
                    'extract_number': extract_number,
                })
                transactions.append(transaction)
        return transactions

    def coda_parsing(self, coda_file):
        recordlist = coda_file.split('\n')
        coda_statements = []
        statements = []
        self.global_comm = {}
        currency_code = False
        account_number = False
        for line in recordlist:
            self._parse_line(line, coda_statements)
        for coda_st in coda_statements:
            if coda_st.get('currency') and not(currency_code):
                currency_code = coda_st['currency']
            if coda_st.get('acc_number') and not(account_number):
                account_number = coda_st['acc_number']
            coda_st['coda_note'] = ''
            if not(coda_st.get('date')):
                raise ValidationError(_(' No transactions or no period in coda file !'))
            statements.append({
                'name': coda_st['paperSeqNumber'],
                'date': coda_st['date'],
                'balance_start': coda_st['balance_start'],
                'balance_end_real': coda_st['balance_end_real'],
                'transactions': self._get_transactions(coda_st),
            })
        return (currency_code, account_number, statements)


class AccountBankStatementLine(models.Model):
    _inherit = "account.bank.statement.line"
 
    extract_number = fields.Char(string='Extract number', readonly=True, copy=False)

class AccountBankStatementImport(models.TransientModel):
    _inherit = 'account.bank.statement.import'

    def _is_coda(self, data_file):
        """Test if `datafile` contains a CODA file"""
        try:
            for line in filter(None, data_file.split('\n')):
                if line[0] == '0':
                    st = {}
                    CodaImport()._parse_line_0(line, st)
                    return st.get('version') in ['1', '2']
                else:
                    return False
        except:
            return False

    def _parse_file(self, data_file):
        """ Each module adding a file support must extends this method. It processes the file if it can, returns super
            otherwise, resulting in a chain of responsability.
            This method parses the given file and returns the data required by the bank statement import process,
            as specified below.
            rtype: triplet (if a value can't be retrieved, use None)
                - currency code: string (e.g: 'EUR')
                    The ISO 4217 currency code, case insensitive
                - account number: string (e.g: 'BE1234567890')
                    The number of the bank account which the statement belongs to
                - bank statements data: list of dict containing (optional items marked by o) :
                    - 'name': string (e.g: '000000123')
                    - 'date': date (e.g: 2013-06-26)
                    -o 'balance_start': float (e.g: 8368.56)
                    -o 'balance_end_real': float (e.g: 8888.88)
                    - 'transactions': list of dict containing :
                        - 'name': string (e.g: 'KBC-INVESTERINGSKREDIET 787-5562831-01')
                        - 'date': date
                        - 'amount': float
                        - 'unique_import_id': string
                        -o 'account_number': string
                            Will be used to find/create the res.partner.bank in odoo
                        -o 'note': string
                        -o 'partner_name': string
                        -o 'ref': string

        The journal to use is deducted from the bank account for which we import the statements
        """
        if self._is_coda(data_file):
            return CodaImport().coda_parsing(data_file)
        return super(AccountBankStatementImport, self)._parse_file(data_file)
