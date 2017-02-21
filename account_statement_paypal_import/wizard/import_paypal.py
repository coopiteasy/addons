# -*- coding: utf-8 -*-
'''
Created on 27 january 2017

@author: Houssine BAKKALI (houssine.bakkali@gmail.com)
'''
from StringIO import StringIO
import csv
import datetime

from openerp import models, _

#ACCOUNT = "Compte donneur d'ordre"
CURRENCY = "Devise"
DATE = "Date"
AMOUNT = "Net"
#COUNTERPART_NUMBER = "Compte contrepartie"
COUNTERPART_NAME = "Nom"
COMMUNICATION = "Num\xc3\xa9ro de transaction"
TRANSACTION_TYPE = "Type"
PARTNER_NAME = "Nom"
PAYPAL_PAYMENT_TYPE = "\xc3\x89tat"
EMAIL_FROM = "De l\x27adresse email"
EMAIL_TO = "\xc3\x80 l\x27adresse email"
TRANSACTION_NUMBER = "Num\xc3\xa9ro de transaction"
TRANSACTION_STATE = "\xc3\x89tat"

class PaypalBankStatementImport(models.TransientModel):
    _inherit = 'account.bank.statement.import'
    
    _date_format = "%d/%m/%Y"

    _decimal_sep = "."
    _csv_delimiter = ","
    _csv_quote = '"'

    #_header = [u"Date",u"Heure",u"Fuseau horaire",u"Nom",u"Type",u"État",u"Devise",u"Avant commission",u"Commission",u"Net",u"De l'adresse email",u"À l'adresse email",u"Numéro de transaction",u"État de l'adresse",u"Titre de l'objet",u"Numéro de l'objet",u"TVA",u"Nom de l'option 1",u"Valeur de l'option 1",u"Nom de l'option 2",u"Valeur de l'option 2",u"Numéro de tiers de confiance",u"Numéro de la transaction de référence",u"Numéro de facture",u"Numéro de client",u"Quantité",u"Numéro de reçu",u"Solde",u"Numéro de téléphone du contact",u"Objet",u"Remarque",u"Source de paiement",u"Type de carte",u"Code de transaction",u"N° du suivi des paiements",u"Identifiant bancaire",u"Code du pays de l'acheteur pour cette transaction",u"Détails de l'objet",u"Balance Impact"]
    _header = ["Date","Heure","Fuseau horaire","Nom","Type","État","Devise","Avant commission","Commission","Net","De l'adresse email","À l'adresse email","Numéro de transaction","État de l'adresse","Titre de l'objet","Numéro de l'objet","TVA","Nom de l'option 1","Valeur de l'option 1","Nom de l'option 2","Valeur de l'option 2","Numéro de tiers de confiance","Numéro de la transaction de référence","Numéro de facture","Numéro de client","Quantité","Numéro de reç","Solde","Numéro de téléphone du contact","Objet","Remarque","Source de paiement","Type de carte","Code de transaction","N° du suivi des paiements","Identifiant bancaire","Code du pays de l'acheteur pour cette transaction","Détails de l'objet","Balance Impact"]
    
    def _generate_note_paypal(self, move):
        notes = []
        notes.append("%s: %s" % (_('Counter Party Name'), move[COUNTERPART_NAME]))
        notes.append("%s: %s" % (_('Counter Party Account'), move[EMAIL_FROM]))
        notes.append("%s: %s" % (_('Communication'), move[COMMUNICATION]))
        return '\n'.join(notes)

    def _get_move_value_paypal(self, move, sequence):
        move_data = {
            'name': move[TRANSACTION_TYPE] + " - " + move[PARTNER_NAME] + ": " + move[COMMUNICATION],
            'note': self._generate_note_paypal(move),
            'date': self._to_iso_date(move[DATE]),
            'amount': float(move[AMOUNT]),
            'account_number': move[EMAIL_FROM], #ok
            'partner_name': move[COUNTERPART_NAME], #ok
            'ref': move[DATE] + '-' + move[AMOUNT] + '-' + move[EMAIL_FROM] + '-' + move[COUNTERPART_NAME],
            'sequence': sequence, #ok
            'unique_import_id' : move[DATE] + '-' + move[AMOUNT] + '-' + move[EMAIL_FROM] + '-' + move[COUNTERPART_NAME] + '-' + move[TRANSACTION_NUMBER],
            'paypal_payment_type':  move[PAYPAL_PAYMENT_TYPE],
            'email_from': move[EMAIL_FROM],
            'email_to': move[EMAIL_TO],
            'transaction_number': move[TRANSACTION_NUMBER],
            'transaction_state': move[TRANSACTION_STATE],
        }
        return move_data

    def _get_statement_data_paypal(self, balance_start, balance_end, begin_date, end_date):
        statement_data = {
            'name' : _("Bank Statement from %s to %s")  % (begin_date, end_date),
            'date' : self._to_iso_date(end_date),
            'balance_start': balance_start, #ok
            'balance_end_real' : balance_end, #ok
            'transactions' : []
        }
        return statement_data
    
    def _get_acc_number_paypal(self, acc_number):
        #Check if we match the exact acc_number(paypal_account) or the end of an acc number
        journal = self.env['account.journal'].search([('bank_acc_number', '=like', '%' + acc_number)])
        if not journal or len(journal) > 1: #if not found or ambiguious 
            return acc_number
        
        return journal.bank_acc_number

    def _get_acc_balance_paypal(self, acc_number):
        if not self.init_balance == None:
            return self.init_balance
        print "compute balance"

        journal = self.env['account.journal'].search([('bank_acc_number', '=like', '%' + acc_number)])
        if not journal or len(journal) > 1: #if not found or ambiguious 
            self.init_balance = 0.0
        else:
            self.init_balance = float(journal.get_journal_dashboard_datas()['last_balance'][:-1].strip().replace(',', ''))
        
        return self.init_balance

    def _to_iso_date(self, orig_date):
        date_obj = datetime.datetime.strptime(orig_date, self._date_format)  
        return date_obj.strftime('%Y-%m-%d')
    
    def _parse_file(self, data_file):

        try:
            csv_file = StringIO(data_file)
            data = csv.DictReader(csv_file, delimiter=self._csv_delimiter, quotechar=self._csv_quote)
            if not data.fieldnames not in self._header:
                raise ValueError()
        except ValueError:
            return super(PaypalBankStatementImport, self)._parse_file(data_file)

        currency_code = False
        account_number = False
        self.init_balance = None
        begin_date = False
        end_date = False
        
        transactions = []
        i = 1
        sum_transaction  = 0
        for statement in data:
            begin_date = begin_date or statement[DATE]
            end_date = statement[DATE]
            account_number =  statement[EMAIL_TO]
            balance = self._get_acc_balance_paypal(account_number)
            currency_code = statement[CURRENCY]
            transactions.append(self._get_move_value_paypal(statement, i))
            sum_transaction += float(statement[AMOUNT])
            i += 1
        stmt = self._get_statement_data_paypal(balance, balance+ sum_transaction, begin_date, end_date)
        stmt['transactions'] = transactions
        return currency_code, self._get_acc_number_paypal(account_number), [stmt]