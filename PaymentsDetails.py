
import os
import webapp2
import jinja2
from google.appengine.ext import ndb
from google.appengine.api import users
import logging
import datetime
template_env = jinja2.Environment(
loader=jinja2.FileSystemLoader(os.getcwd()))


# Direct Deposit - Cash - Payroll Deduction - Debit Order - Persal Deduction - Intermediary
class PaymentID(ndb.Expando):
    strPolicyNum = ndb.StringProperty()
    strSignedAuthorisation = ndb.BlobKeyProperty()
    undefined = None

    def readSignedAuthorisation(self):
        try:
            strTemp = self.strSignedAuthorisation
            return strTemp
        except:
            return self.undefined

    def writeSignedAuthorisation(self,strinput):
        try:
            if not(strinput == self.undefined):
                self.strSignedAuthorisation = strinput
                return True
            else:
                return False

        except:
            return False
    def readPolicyNumber(self):
        try:
            strTemp = str(self.strPolicyNum)
            strTemp = strTemp.strip()
            return strTemp
        except:
            return self.undefined

    def writePolicyNumber(self,strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if not(strinput == self.undefined):
                self.strPolicyNum = strinput
                return True
            else:
                return False
        except:
            return False

class DirectDeposit(PaymentID):

    strDepositReference = ndb.StringProperty() # The Client will use this reference number on the deposit slip

    def readDepositReference(self):
        try:
            strTemp = str(self.strDepositReference)
            strTemp = strTemp.strip()
            return strTemp
        except:
            return self.undefined

    def writeDepositReference(self,strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if not(strinput == self.undefined):
                self.strDepositReference = strinput
                return True
            else:
                return False

        except:
            return False


class Cash(PaymentID):
    strReceiptNumber = ndb.StringProperty()

    def readReceiptNumber(self):
        try:
            strTemp = str(self.strReceiptNumber)
            strTemp = strTemp.strip()
            return strTemp
        except:
            return self.undefined

    def writeReceiptNumber(self,strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if not(strinput == self.undefined):
                self.strReceiptNumber = strinput
                return True
            else:
                return False

        except:
            return False


class DebitOrder(PaymentID):

    strBankName = ndb.StringProperty()
    strBranchCode = ndb.StringProperty()
    strAccountType = ndb.StringProperty()
    strAccountHolder = ndb.StringProperty()
    strAccountNumber = ndb.StringProperty()




    def readBankName(self):
        try:
            strTemp =str(self.strBankName)
            strTemp = strTemp.strip()

            return strTemp
        except:
            return self.undefined
    def writeBankName(self,strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if not(strinput == self.undefined):
                self.strBankName = strinput
                return True
            else:
                return False
        except:
            return False

    def readBranchCode(self):
        try:
            strTemp = str(self.strBranchCode)
            strTemp = strTemp.strip()

            if strTemp.isdigit():
                return strTemp
            else:
                return self.undefined
        except:
            return self.undefined
    def writeBranchCode(self,strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if strinput.isdigit():
                self.strBranchCode = strinput
                return True
            else:
                return False

        except:
            return False

    def readAccountType(self):
        try:
            strTemp = str(self.strAccountType)
            strTemp = strTemp.strip()

            if (strTemp.lower() == "savings") or (strTemp.lower() == "cheque") or (strTemp.lower() == "transmission"):
                return strTemp
            else:
                return self.undefined
        except:
            return self.undefined
    def writeAccountType(self,strinput):
        try:
            strinput = str(strinput).strip()
            strinput = strinput.lower()

            if (strinput == "savings") or (strinput == "cheque") or (strinput == "transmission"):
                self.strAccountType = strinput
                return True
            else:
                return False

        except:
            return False

    def readAccountHolder(self):
        try:
            strTemp = str(self.strAccountHolder)
            strTemp = strTemp.strip()

            return strTemp
        except:
            return self.undefined
    def writeAccountHolder(self,strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if not(strinput == self.undefined):
                self.strAccountHolder = strinput
                return True
            else:
                return False

        except:
            return False

    def readAccountNumber(self):
        try:
            strTemp = str(self.strAccountNumber)
            strTemp = strTemp.strip()

            if strTemp.isdigit():
                return strTemp
            else:
                return self.undefined
        except:
            return self.undefined
    def writeAccountNumber(self,strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if strinput.isdigit():
                self.strAccountNumber == strinput
                return True
            else:
                return False

        except:
            return False





