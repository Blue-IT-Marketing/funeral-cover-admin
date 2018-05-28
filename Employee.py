import os
import webapp2
import jinja2
from google.appengine.ext import ndb
from google.appengine.api import users
import logging
import datetime
template_env = jinja2.Environment(
loader=jinja2.FileSystemLoader(os.getcwd()))

class EmployeeConst(ndb.Expando):
    undefined = None
    _generalError = "General Error"
    strEmployeeCode = ndb.StringProperty(default='E01')
    strReference = ndb.StringProperty()

    def readEmployeeCode(self):
        try:
            strTemp = str(self.strEmployeeCode)
            strTemp = strTemp.strip()

            if not (strTemp == self.undefined):
                return strTemp
            else:
                return ""
        except:
            return ""

    def writeEmployeeCode(self,strinput):
        try:

            strinput = str(strinput)
            strinput = strinput.strip()

            if not (strinput == self.undefined):
                self.strEmployeeCode = strinput
                return True
            else:
                return False
        except:
            return False

    def readReference(self):
        try:
            strTemp = str(self.strReference)
            strTemp = strTemp.strip()

            if not(strTemp == self.undefined):
                return strTemp
            else:
                return ""
        except:
            return ""

    def writeReference(self,strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if not(strinput == self.undefined):
                self.strReference = strinput
                return True
            else:
                return False
        except:
            return self._generalError

class EmployeeRegRequest(ndb.Expando):
    strEmail = ndb.StringProperty()
    strReference = ndb.StringProperty()
    strIDNumber = ndb.StringProperty()


    def readEmail(self):
        try:
            strTemp = str(self.strEmail)
            strTemp = strTemp.strip()

            if not(strTemp == None):
                return strTemp
            else:
                return ""
        except:
            return ""

    def writeEmail(self,strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if not(strinput == None):
                self.strEmail = strinput
                return True
            else:
                return False
        except:
            return False

    def readReference(self):
        try:
            strTemp = str(self.strReference)
            strTemp = strTemp.strip()

            if not(strTemp == None):
                return strTemp
            else:
                return ""
        except:
            return ""

    def writeReference(self,strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if not(strinput == None):
                self.strReference = strinput
                return True
            else:
                return False
        except:
            return False

    def writeIDNumber(self,strinput):
        try:
            strinput = str(strinput)

            if strinput.isdigit():
                self.strIDNumber = strinput
                return True
            else:
                return False
        except:
            return False

    def readIDNumber(self):
        try:
            strTemp = str(self.strIDNumber)
            strTemp = strTemp.strip()

            if strTemp.isdigit():
                return strTemp
            else:
                return ""
        except:
            return ""

class CompanyDetails(EmployeeConst):
    pass

class BranchDetails(EmployeeConst):
    """
        When Setting Up Branch Names and Codes must be entered on the Admin Interface of the WebApp
    """
    strCompanyBranchCode = ndb.StringProperty()
    strCompanyBranchName = ndb.StringProperty()
    strCompanyBranchAddress = ndb.StringProperty()
    strCompanyBranchTel = ndb.StringProperty()
    strCompanyBranchEmail = ndb.StringProperty()
    strCompanyBranchManagerName = ndb.StringProperty()
    strCompanyBranchManagerTel = ndb.StringProperty()
    strCompanyBranchManagerEmail = ndb.StringProperty()



    def readCompanyBranchCode(self):
        try:
            strTemp = str(self.strCompanyBranchCode)
            strTemp = strTemp.strip()

            if not(strTemp == self.undefined):
                return strTemp
            else:
                return ""
        except:
            return ""

    def writeCompanyBranchCode(self,strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if not(strinput == self.undefined):
                self.strCompanyBranchCode = strinput
                return True
            else:
                return False
        except:
            return self._generalError

    def readCompanyBranchName(self):
        try:
            strTemp = str(self.strCompanyBranchName)
            strTemp = strTemp.strip()

            if not(strTemp == self.undefined):
                return strTemp
            else:
                return ""
        except:
            return ""

    def writeCompanyBranchName(self,strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if not(strinput == self.undefined):
                self.strCompanyBranchName = strinput
                return True
            else:
                return False
        except:
            return self._generalError

    def writeCompanyBranchAddress(self,strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if not(strinput == self.undefined):
                self.strCompanyBranchAddress = strinput
                return True
            else:
                return False
        except:
            return self._generalError

    def readCompanyBranchAddress(self):
        try:
            strTemp = str(self.strCompanyBranchAddress)
            strTemp = strTemp.strip()

            if not(strTemp == self.undefined):
                return strTemp
            else:
                return ""
        except:
            return ""

    def writeCompanyBranchTel(self,strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if not(strinput == self.undefined):
                self.strCompanyBranchTel = strinput
                return True
            else:
                return False
        except:
            return self._generalError

    def readCompanyBranchTel(self):
        try:
            strTemp = str(self.strCompanyBranchTel)
            strTemp = strTemp.strip()

            if not(strTemp == self.undefined):
                return strTemp
            else:
                return ""
        except:
            return ""

    def writeCompanyBranchEmail(self,strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if not(strinput == self.undefined):
                self.strCompanyBranchEmail = strinput
                return True
            else:
                return False
        except:
            return self._generalError

    def readCompanyBranchEmail(self):
        try:
            strTemp = str(self.strCompanyBranchEmail)
            strTemp = strTemp.strip()

            if not(strTemp == self.undefined):
                return strTemp
            else:
                return ""
        except:
            return ""

    def writeBranchManagerName(self,strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if not(strinput == self.undefined):
                self.strCompanyBranchManagerName = strinput
                return True
            else:
                return False
        except:
            return self._generalError

    def readBranchManagerName(self):
        try:
            strTemp = str(self.strCompanyBranchManagerName)
            strTemp = strTemp.strip()
            if not(strTemp == self.undefined):
                return strTemp
            else:
                return ""
        except:
            return ""

    def writeBranchManagerTel(self,strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if not(strinput == self.undefined):
                self.strCompanyBranchManagerTel = strinput
                return True
            else:
                return False
        except:
            return self._generalError

    def readBrachManagerTel(self):
        try:
            strTemp = str(self.strCompanyBranchManagerTel)
            strTemp = strTemp.strip()

            if not(strTemp == self.undefined):
                return strTemp
            else:
                return ""
        except:
            return ""

    def writeBranchManagerEmail(self,strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if not(strinput == self.undefined):
                self.strCompanyBranchManagerEmail = strinput
                return True
            else:
                return False
        except:
            return self._generalError

    def readBranchManagerEmail(self):
        try:
            strTemp = str(self.strCompanyBranchManagerEmail)
            strTemp = strTemp.strip()

            if not(strTemp == self.undefined):
                return strTemp
            else:
                return ""
        except:
            return ""

class PersonalDetails(EmployeeConst):

    strTitle = ndb.StringProperty()
    strFullNames = ndb.StringProperty()
    strSurname = ndb.StringProperty()
    strIDNumber = ndb.StringProperty() # Passport Number
    strDateOfBirth = ndb.DateProperty()
    strNationality = ndb.StringProperty()


    def readTitle(self):
        try:
            strtemp = str(self.strTitle)
            strtemp = strtemp.strip()

            if not (strtemp == self.undefined):
                return strtemp
            else:
                return ""

        except:
            return ""

    def writeTitle(self, strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if not (strinput == self.undefined):
                self.strTitle = strinput
                return True
            else:
                return False
        except:
            return self._generalError

    def writeNames(self,strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if not(strinput == self.undefined):
                self.strFullNames = strinput
                return True
            else:
                return False
        except:
            return self._generalError

    def readNames(self):
        try:
            strTemp = str(self.strFullNames)
            strTemp = strTemp.strip()

            if not(strTemp == self.undefined):
                return strTemp
            else:
                return ""
        except:
            return ""

    def readSurname(self):
        try:
            strTemp = str(self.strSurname)
            strTemp = strTemp.strip()

            if not (strTemp == self.undefined):
                return strTemp
            else:
                return ""
        except:
            return ""

    def writeSurname(self, strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if not (strinput == self.undefined):
                self.strSurname = strinput
                return True
            else:
                return False
        except:
            return self._generalError

    def readIDNumber(self):
        try:
            strTemp = str(self.strIDNumber)
            strTemp = strTemp.strip()

            if not (strTemp == self.undefined):
                return strTemp
            else:
                return ""
        except:
            return ""

    def writeIDNumber(self, strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if not (strinput == self.undefined):
                self.strIDNumber = strinput
                return True
            else:
                return False
        except:
            return self._generalError

    def readDateOfBirth(self):
        try:
            strtemp = str(self.strDateOfBirth)

            if not (strtemp == self.undefined):
                return strtemp
            else:
                return ""
        except:
            return ""

    def writeDateOfBirth(self, strinput):
        """
            format yyyy-mm-dd
        """
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            Datefields = strinput.split("-")

            if len(Datefields) == 3:
                tempDate = datetime.date(year=int(Datefields[0]),month=int(Datefields[1]),day=int(Datefields[2]))
                self.strDateOfBirth = tempDate
                return True
            else:
                return False
        except:
            return self._generalError

    def readNationality(self):
        try:
            strTemp = str(self.strNationality)
            strTemp = strTemp.strip()

            if not (strTemp == self.undefined):
                return strTemp
            else:
                return ""
        except:
            return ""

    def writeNationality(self, strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if not (strinput == self.undefined):
                self.strNationality = strinput
                return True
            else:
                return False
        except:
            return self._generalError

class ResidentialAddress(EmployeeConst):

    strResAddressLine1 = ndb.StringProperty()
    strResAddressLine2 = ndb.StringProperty()
    strCountry = ndb.StringProperty()
    strTownCity = ndb.StringProperty()
    strProvince = ndb.StringProperty()
    strPostalCode = ndb.StringProperty()



    def readResAddressL1(self):
        try:
            strTemp = str(self.strResAddressLine1)
            strTemp = strTemp.strip()

            if not(strTemp == self.undefined):
                return strTemp
            else:
                return ""
        except:
            return ""

    def writeResAddressL1(self,strinput):
        try:
            strinput = str(strinput)
            strinput =strinput.strip()

            if not(strinput == self.undefined):
                self.strResAddressLine1 = strinput
                return True
            else:
                return False
        except:
            return self._generalError

    def readResAddressL2(self):
        try:
            strTemp = str(self.strResAddressLine2)
            strTemp = strTemp.strip()

            if not(strTemp == self.undefined):
                return strTemp
            else:
                return ""
        except:
            return ""

    def writeResAddressL2(self,strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if not(strinput == self.undefined):
                self.strResAddressLine2 = strinput
                return True
            else:
                return False
        except:
            return self._generalError

    def readCityTown(self):
        try:
            strTemp = str(self.strTownCity)
            strTemp = strTemp.strip()

            if not(strTemp == self.undefined):
                return strTemp
            else:
                return ""
        except:
            return ""

    def writeCityTown(self,strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if not(strinput == self.undefined):
                self.strTownCity = strinput
                return True
            else:
                return False
        except:
            return self._generalError

    def readCountry(self):
        try:
            strTemp = str(self.strCountry)
            strTemp = strTemp.strip()

            if not(strTemp == self.undefined):
                return strTemp
            else:
                return ""
        except:
            return ""

    def writeCountry(self,strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if not(strinput == self.undefined):
                self.strCountry = strinput
                return True
            else:
                return False
        except:
            return self._generalError

    def readProvince(self):
        try:
            strTemp = str(self.strProvince)
            strTemp =strTemp.strip()

            if not(strTemp == self.undefined):
                return strTemp
            else:
                return ""
        except:
            return ""

    def writeProvince(self,strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if not(strinput == self.undefined):
                self.strProvince = strinput
                return True
            else:
                return False
        except:
            return self._generalError

    def readPostalCode(self):
        try:
            strTemp = str(self.strPostalCode)
            strTemp = strTemp.strip()

            if not(strTemp == self.undefined):
                return strTemp
            else:
                return ""
        except:
            return ""

    def writePostalCode(self,strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if not(strinput == self.undefined):
                self.strPostalCode = strinput
                return True
            else:
                return False
        except:
            return self._generalError

class PostalAddress(EmployeeConst):

    strPostalAddressLine1 = ndb.StringProperty()
    strPostalAddressLine2 = ndb.StringProperty()
    strCountry = ndb.StringProperty()
    strTownCity = ndb.StringProperty()
    strProvince = ndb.StringProperty()
    strPostalCode = ndb.StringProperty()

    def readPostalAddressL1(self):
        try:
            strTemp = str(self.strPostalAddressLine1)
            strTemp = strTemp.strip()

            if not(strTemp == self.undefined):
                return strTemp
            else:
                return ""
        except:
            return ""

    def writePostalAddressL1(self,strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if not(strinput == self.undefined):
                self.strPostalAddressLine1 = strinput
                return True
            else:
                return False
        except:
            return self._generalError

    def readPostalAddressL2(self):
        try:
            strTemp = str(self.strPostalAddressLine2)
            strTemp = strTemp.strip()

            if not(strTemp == self.undefined):
                return strTemp
            else:
                return ""
        except:
            return ""

    def writePostalAddressL2(self,strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if not(strinput == self.undefined):
                self.strPostalAddressLine2 = strinput
                return True
            else:
                return False
        except:
            return self._generalError

    def readCountry(self):
        try:
            strTemp = str(self.strCountry)
            strTemp = strTemp.strip()

            if not(strTemp == self.undefined):
                return strTemp
            else:
                return ""
        except:
            return ""

    def writeCountry(self,strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if not(strinput == self.undefined):
                self.strCountry = strinput
                return True
            else:
                return False
        except:
            return self._generalError

    def readTownCity(self):
        try:
            strTemp = str(self.strTownCity)
            strTemp = strTemp.strip()

            if not(strTemp == self.undefined):
                return strTemp
            else:
                return ""
        except:
            return ""

    def writeTownCity(self,strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if not(strinput == self.undefined):
                self.strTownCity = strinput
                return True
            else:
                return False
        except:
            return self._generalError

    def readProvince(self):
        try:
            strTemp = str(self.strProvince)
            strTemp = strTemp.strip()

            if not(strTemp == self.undefined):
                return strTemp
            else:
                return ""
        except:
            return ""

    def writeProvince(self,strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if not(strinput == self.undefined):
                self.strProvince = strinput
                return True
            else:
                return False
        except:
            return self._generalError

    def readPostalCode(self):
        try:
            strTemp = str(self.strPostalCode)
            strTemp = strTemp.strip()

            if not(strTemp == self.undefined):
                return strTemp
            else:
                return ""
        except:
            return ""

    def writePostalCode(self,strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()


            if not(strinput == self.undefined):
                self.strPostalCode = strinput
                return True
            else:
                return False
        except:
            return self._generalError

class ContactDetails(EmployeeConst):
    """
        # Reference of CLient If relate to a policy and policy number will be shown
        # Reference of employee if its contact of an employee
    """

    strCell = ndb.StringProperty()
    strTel = ndb.StringProperty()
    strEmail = ndb.StringProperty()

    def readCell(self):
        try:
            strTemp = str(self.strCell)
            strTemp = strTemp.strip()

            if not(strTemp == self.undefined):
                return strTemp
            else:
                return ""
        except:
            return ""

    def writeCell(self,strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if not(strinput == self.undefined):
                self.strCell = strinput
                return True
            else:
                return False
        except:
            return ""

    def readTell(self):
        try:
            strTemp = str(self.strTel)
            strTemp = strTemp.strip()

            if not(strTemp == self.undefined):
                return strTemp
            else:
                return ""
        except:
            return ""

    def writeTel(self,strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if not(strinput == self.undefined):
                self.strTel = strinput
                return True
            else:
                return False
        except:
            return self._generalError

    def readEmail(self):
        try:
            strTemp = str(self.strEmail)
            strTemp = strTemp.strip()

            if not(strTemp == self.undefined):
                return strTemp
            else:
                return ""
        except:
            return ""

    def writeEmail(self,strinput):
        try:
            strinput = str(strinput)
            if not(strinput == self.undefined):
                self.strEmail = strinput
                return True
            else:
                return False
        except:
            return self._generalError

class BankingDetails(EmployeeConst):
    """
        Banking Details will also take in banking details of the Employees and also that of the Clients.
    """
    strBankName = ndb.StringProperty()
    strAccountHolder = ndb.StringProperty()
    strAccountNumber = ndb.StringProperty()
    strAccountType = ndb.StringProperty(default='savings')
    strBranchCode = ndb.StringProperty()

    def readBankName(self):
        try:
            strTemp = str(self.strBankName)
            strTemp = strTemp.strip()

            if not(strTemp == self.undefined):
                return strTemp
            else:
                return ""
        except:
            return ""

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
            return self._generalError

    def readAccountHolder(self):
        try:
            strTemp = str(self.strAccountHolder)
            strTemp = strTemp.strip()

            if not(strTemp == self.undefined):
                return strTemp
            else:
                return ""
        except:
            return ""

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
            return self._generalError

    def readAccountNumber(self):
        try:
            strTemp = str(self.strAccountNumber)
            strTemp = strTemp.strip()

            if not(strTemp == self.undefined):
                return strTemp
            else:
                return ""
        except:
            return ""

    def writeAccountNumber(self,strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if not(strinput == self.undefined):
                self.strAccountNumber = strinput
                return True
            else:
                return False
        except:
            return self._generalError

    def writeAccountType(self,strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if not(strinput == self.undefined):
                self.strAccountType = strinput
                return True
            else:
                return False
        except:
            return self._generalError

    def readAccountType(self):
        try:
            strTemp = str(self.strAccountType)
            strTemp = strTemp.strip()

            if not(strTemp == self.undefined):
                return strTemp
            else:
                return ""
        except:
            return ""

    def readBranchCode(self):
        try:
            strTemp = str(self.strBranchCode)
            strTemp = str(strTemp)

            if not(strTemp == self.undefined):
                return strTemp
            else:
                return ""
        except:
            return ""

    def writeBranchCode(self,strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if not(strinput == self.undefined):
                self.strBranchCode = strinput
                return True
            else:
                return False
        except:
            return self._generalError

class EmploymentDetails(PersonalDetails):
    """
        When Setting Up Employee Names DETAILS and User Rights must be entered from the App Admin Interface
        The User Rights will give access to employees, this access can be removed later and re added when needed
        or when a task at end requires such an access
    """
    strDateOfEmployment = ndb.DateProperty()
    strContractType = ndb.StringProperty(default='permanent')
    strBasicSalary = ndb.IntegerProperty()
    strBranchCode = ndb.StringProperty()

    strSuspendOnPay = ndb.BooleanProperty(default=False)
    strSuspend = ndb.BooleanProperty(default=False)
    str24HourLock = ndb.BooleanProperty(default=False)
    strLockIndefinetely = ndb.BooleanProperty(default=False)

    strNameOfEmployer = ndb.StringProperty()

    strTotalMessages = ndb.IntegerProperty(default=0)



    def readSuspendOnPay(self):
        try:
            return self.strSuspendOnPay
        except:
            return ""

    def writeSuspendOnPay(self,strinput):
        try:

            if (strinput == True):
                self.strSuspendOnPay = True
                return True
            elif (strinput == False):
                self.strSuspendOnPay = False
                return True
            else:
                return False
        except:
            return False

    def writeSuspend(self,strinput):
        try:
            if strinput == True:
                self.strSuspend = True
                return True
            elif strinput == False:
                self.strSuspend = False
                return True
            else:
                return False
        except:
            return False

    def readSuspend(self):
        try:
            return self.strSuspend
        except:
            return ""

    def write24HourLock(self,strinput):
        try:
            if strinput == True:
                self.str24HourLock = True
                return True
            elif strinput == False:
                self.str24HourLock = False
                return True
            else:
                return False
        except:
            return False

    def read24HourLock(self):
        try:
            return self.str24HourLock
        except:
            return ""


    def writeLockUserIndefinetely(self,strinput):
        try:
            if strinput == True:
                self.strLockIndefinetely = True
                return True
            elif strinput == False:
                self.strLockIndefinetely = False
                return True
            else:
                return False
        except:
            return False

    def readLockUserIndefinetely(self):
        try:
            return self.strLockIndefinetely
        except:
            return ""


    def readDateOfEmployment(self):
        """
            format dd/mm/yyyy
        """
        try:
            strTemp = str(self.strDateOfEmployment)
            strTemp = strTemp.strip()

            if not(strTemp == self.undefined):
                return strTemp
            else:
                return ""
        except:
            return ""

    def writeDateOfEmployment(self,strinput):
        """
            format dd/mm/yyyy
        """
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            Datefields = strinput.split("-")

            if len(Datefields) == 3:
                tempDate = datetime.date(year=int(Datefields[0]),month=int(Datefields[1]),day=int(Datefields[2]))
                self.strDateOfEmployment = tempDate
                return True
            else:
                return False
        except:
            return self._generalError

    def readContractType(self):
        try:
            strTemp = str(self.strContractType)
            strTemp = strTemp.strip()

            if not(strTemp == self.undefined):
                return strTemp
            else:
                return ""
        except:
            return ""

    def writeContractType(self,strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if not(strinput == self.undefined):
                self.strContractType = strinput
                return True
            else:
                return False
        except:
            return self._generalError

    def readBasicSalary(self):
        try:
            strTemp = str(self.strBasicSalary)
            strTemp = strTemp.strip()

            if not(strTemp == self.undefined):
                return int(strTemp)
            else:
                return ""
        except:
            return ""

    def writeBasicSalary(self,strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if strinput.isdigit():
                self.strBasicSalary = int(strinput)
                return True
            else:
                return False
        except:
            return self._generalError



    def readBranchWorking(self):
        try:
            strTemp = str(self.strBranchCode)
            strTemp = strTemp.strip()

            if not(strTemp == self.undefined):
                return strTemp
            else:
                return ""
        except:
            return ""

    def writeBranchWorking(self,strinput):
        try:
            strinput = str(strinput)

            if not(strinput == self.undefined):
                self.strBranchCode = strinput
                return True
            else:
                return False
        except:
            return self._generalError

    def readNameEmployer(self):
        try:
            strTemp = str(self.strNameOfEmployer)
            strTemp = strTemp.strip()

            if not(strTemp == self.undefined):
                return strTemp
            else:
                return ""
        except:
            return ""

    def writeNameEmployer(self,strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if not(strinput == self.undefined):
                self.strNameOfEmployer = strinput
                return True
            else:
                return False
        except:
            return self._generalError


class EmployeesHandler(webapp2.RequestHandler):
    def get(self):
        logging.info("Employees Handler Called")
        URL = str(self.request.url)
        logging.info(URL)

        URL = URL.split("/")
        EmpCode = URL[len(URL) - 1]
        logging.info(EmpCode)



        findRequest = EmploymentDetails.query(EmploymentDetails.strEmployeeCode == EmpCode)
        EMPresults = findRequest.fetch()

        if len(EMPresults) > 0:
            EmployeeDet = EMPresults[0]
        else:
            EmployeeDet = EmploymentDetails()

        findRequest = BankingDetails.query(BankingDetails.strEmployeeCode == EmpCode)
        BANKresults = findRequest.fetch()

        if len(BANKresults) > 0:
            Banking = BANKresults[0]
        else:
            Banking = BankingDetails()

        findRequest = ContactDetails.query(ContactDetails.strEmployeeCode == EmpCode)
        CONTresults = findRequest.fetch()

        if len(CONTresults) > 0:
            Contacts = CONTresults[0]
        else:
            Contacts = ContactDetails()

        findRequest = PostalAddress.query(PostalAddress.strEmployeeCode == EmpCode)
        POSresults = findRequest.fetch()

        if len(POSresults) > 0:
            PostalAddY = POSresults[0]
        else:
            PostalAddY = PostalAddress()

        findRequest = ResidentialAddress.query(ResidentialAddress.strEmployeeCode == EmpCode)
        RESresults = findRequest.fetch()

        if len(RESresults) > 0:
            Physical = RESresults[0]
        else:
            Physical = ResidentialAddress()

        findRequest = BranchDetails.query()

        clsbranches = findRequest.fetch()

        context ={'branches': clsbranches ,'vstrBranchCode': EmployeeDet.readBranchWorking(),'vstrEmployeeCode': EmployeeDet.readEmployeeCode(),
                  'vstrContractType': EmployeeDet.readContractType(),'vstrBasicSalary': EmployeeDet.readBasicSalary(),
                  'vstrDateOfEmployment': EmployeeDet.readDateOfEmployment(),'vstrTitle': EmployeeDet.readTitle(),
                  'vstrFullnames': EmployeeDet.readNames(),'vstrSurname': EmployeeDet.readSurname(),
                  'vstrIDNumber':EmployeeDet.readIDNumber(),'vstrDateOfBirth': EmployeeDet.readDateOfBirth(),
                  'vstrNationality':EmployeeDet.readNationality(),'vstrPhysicalAddressL1':Physical.readResAddressL1(),
                  'vstrPhysicalAddressL2': Physical.readResAddressL2(),'vstrCityTown':Physical.readCityTown(),
                  'vstrProvince':Physical.readProvince(),'vstrPhysicalPostalCode': Physical.readPostalCode(),
                  'vstrPostalAddressL1': PostalAddY.readPostalAddressL1(),'vstrPostalCityTown':PostalAddY.readTownCity(),
                  'vstrPostalProvince':PostalAddY.readProvince(),'vstrPostalCode': PostalAddY.readPostalCode(),
                  'vstrCell': Contacts.readCell(),'vstrTel': Contacts.readTell(), 'vstrEmail': Contacts.readEmail(),
                  'vstrAccountHolder': Banking.readAccountHolder(),'vstrBankName': Banking.readBankName(),
                  'vstrAccountType': Banking.readAccountType(), 'vstrAccountNumber': Banking.readAccountNumber(),
                  'vstrBankBranchCode': Banking.readBranchCode(),
                  'vstrSuspendOnPay': str(EmployeeDet.readSuspendOnPay()),
                  'vstrSuspend': str(EmployeeDet.readSuspend()),
                  'vstr24HourLock': str(EmployeeDet.read24HourLock()),
                  'vstrLockIndefinite': str(EmployeeDet.readLockUserIndefinetely())}

        template = template_env.get_template('templates/dynamic/admin/employeeDetails.html')

        self.response.write(template.render(context))



    def post(self):
        URL = self.request.url
        logging.info(URL)

app = webapp2.WSGIApplication([
    ('/admin/employees/.*', EmployeesHandler)

], debug=True)