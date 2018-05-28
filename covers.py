import os
import webapp2
import jinja2
from google.appengine.ext import ndb
from google.appengine.api import users
import logging
template_env = jinja2.Environment(
loader=jinja2.FileSystemLoader(os.getcwd()))

from database import ClientsPersonalDetails, ChildrenDetails , Spouses, ExtendedFamily, Beneficiary,Policy,WorkingPolicy
from datetime import datetime
from Employee import BranchDetails,EmploymentDetails

def yearsago(years, from_date=None):
    if from_date is None:
        from_date = datetime.now()
    try:
        return from_date.replace(year=from_date.year - years)
    except ValueError:
        # Must be 2/29!
        assert from_date.month == 2 and from_date.day == 29 # can be removed
        return from_date.replace(month=2, day=28,
                                 year=from_date.year-years)
def num_years(begin, end=None):
    if end is None:
        end = datetime.now()
    num_years = int((end - begin).days / 365.2425)
    if begin > yearsago(num_years, end):
        return num_years - 1
    else:
        return num_years

class Constant(ndb.Model):
    strReference = ndb.StringProperty()
    undefined = None
    _generalError = "General Error"

    def readReference(self):
        try:
            strTemp = str(self.strReference)
            strTemp = strTemp.strip()

            if not(strTemp == self.undefined):
                return strTemp
            else:
                return self.undefined
        except:
            return self._generalError

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

class PlanRules(Constant):
    """
        Same Person cannot be a dependent in more than one cover...
        Meaning a person cannot receive double claims.
    """
    strCoverCode = ndb.StringProperty()
    strPaymentDates = ndb.DateProperty(repeated=True)
    strNumDaysToLapse = ndb.IntegerProperty(default=3)
    strInterestonLapse = ndb.IntegerProperty(default=0)
    strGracePeriod = ndb.IntegerProperty(default=3)
    strClaimPayoutPeriod = ndb.IntegerProperty(default=48)


    def readCoverCode(self):
        try:
            strTemp = str(self.strCoverCode)
            strTemp = strTemp.strip()

            if (strTemp == self.undefined):
                return strTemp
            else:
                return self.undefined
        except:
            return self._generalError

    def writeCoverCode(self,strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if not(strinput == self.undefined):
                self.strCoverCode = strinput
                return True
            else:
                return False
        except:
            return self._generalError

    def readPaymentDates(self):
        try:
            strTemp = self.strPaymentDates

            if len(strTemp) > 0:
                return strTemp
            else:
                return self.undefined
        except:
            return self._generalError

    def writePaymentDates(self,clsinput):
        """
            clsinput is an array with Different Payment Dates
        :param clsinput:
        :return True:
        """
        try:
            if not(clsinput == []):
                self.strPaymentDates = clsinput
                return True
            else:
                return False

        except:
            return self._generalError

    def readNumDaysLapse(self):
        try:
            strTemp = str(self.strNumDaysToLapse)
            strTemp = strTemp.strip()

            if not(strTemp == self.undefined):
                return int(strTemp)
            else:
                return self.undefined
        except:
            return self._generalError

    def writeNumDaysLapse(self,strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if strinput.isdigit():
                self.strNumDaysToLapse = int(strinput)
                return True
            else:
                return False
        except:
            return self._generalError

    def readInterestOnLapse(self):
        try:
            strTemp = str(self.strInterestonLapse)
            strTemp = strTemp.strip()

            if strTemp.isdigit():
                return int(strTemp)
            else:
                return self.undefined

        except:
            return self._generalError

    def writeInterestOnLapse(self,strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if strinput.isdigit():
                self.strInterestonLapse = int(strinput)
                return True
            else:
                return False
        except:
            return self._generalError

    def readGracePeriod(self):
        try:
            strTemp = str(self.strGracePeriod)
            strTemp = strTemp.strip()

            if strTemp.isdigit():
                return int(strTemp)
            else:
                return self.undefined
        except:
            return self._generalError

    def writeGracePeriod(self,strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if strinput.isdigit():
                self.strGracePeriod = strinput
                return True
            else:
                return False

        except:
            return self._generalError

    def readClaimPayoutPeriod(self):
        try:
            strTemp = str(self.strClaimPayoutPeriod)
            strTemp = strTemp.strip()

            if strTemp.isdigit():
                return strTemp
            else:
                return self.undefined
        except:
            return self._generalError

    def writeClaimPayoutPeriod(self,strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if strinput.isdigit():
                self.strClaimPayoutPeriod = strinput
                return True
            else:
                return False
        except:
            return self._generalError
class PlanRows(Constant):
    """
      Structure of Cover
      Rows[0] = Row Name e.g Policy Holder / Spouse
      Rows[1] = Int Value for lower Year Range
      Rows[2] = Int Value for Upper Year Range
      Rows[3 - 6] = Int Value for the Payouts Values

      Premium Rows
      rows[0 - 3] = int Value Representing Monthly Premiums
    """
    strCoverCode = ndb.StringProperty()
    strPlanRowNumber = ndb.IntegerProperty(default=0)
    strPLanColNumber = ndb.IntegerProperty(default=0)

    strMemberType = ndb.StringProperty() # Family / Spouse / Children / School / Still Born
    strYearLow = ndb.IntegerProperty(default=18)
    strYearHigh = ndb.IntegerProperty(default=60)
    strPremium = ndb.IntegerProperty(default=50)
    strPayout = ndb.IntegerProperty(default=5000)

    def readCoverCode(self):
        try:
            strTemp = str(self.strCoverCode)
            strTemp = strTemp.strip()

            if (strTemp == self.undefined):
                return strTemp
            else:
                return self.undefined
        except:
            return self._generalError

    def writeCoverCode(self,strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if not(strinput == self.undefined):
                self.strCoverCode = strinput
                return True
            else:
                return False
        except:
            return self._generalError

    def readPlanRowNumber(self):
        try:
            strTemp = str(self.strPlanRowNumber)

            if strTemp.isdigit():
                return strTemp
            else:
                return self.undefined
        except:
            return self._generalError

    def writePlanRowNumber(self,strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if strinput.isdigit():
                self.strPlanRowNumber = int(strinput)
                return True
            else:
                return False
        except:
            return False

    def readPlanColNumber(self):
        try:

            strTemp = str(self.strPLanColNumber)
            strTemp = strTemp.strip()

            if strTemp.isdigit():
                return int(strTemp)
            else:
                return self.undefined
        except:
            return self._generalError

    def writePlanColNumber(self,strinput):
        try:

            strinput = str(strinput)
            strinput = strinput.strip()

            if strinput.isdigit():
                self.strPLanColNumber = int(strinput)
                return True
            else:
                return False
        except:
            return False

    def readMemberType(self):
        try:

            strTemp = str(self.strMemberType)
            strTemp = strTemp.strip()
            strTemp = strTemp.lower()

            if not(strTemp == self.undefined):
                return strTemp
            else:
                return self.undefined
        except:
            return self._generalError

    def writeMemberType(self,strinput):

        try:

            strinput = str(strinput)
            strinput = strinput.strip()

            if not(strinput == self.undefined):
                self.strMemberType = strinput
                return True
            else:
                return False

        except:
            return False

    def readYearLow(self):
        try:

            strTemp = str(self.strYearLow)
            strTemp = strTemp.strip()

            if strTemp.isdigit():
                return int(strTemp)
            else:
                return self.undefined
        except:
            return self._generalError

    def writeYearLow(self,strinput):

        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if strinput.isdigit():
                self.strYearLow = int(strinput)
                return True
            else:
                return False
        except:
            return False

    def readYearHigh(self):
        try:

            strTemp = str(self.strYearHigh)
            strTemp = str(strTemp)

            if strTemp.isdigit():
                return int(strTemp)
            else:
                return self.undefined
        except:
            return self._generalError

    def writeYearHigh(self,strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if strinput.isdigit():
                self.strYearHigh = int(strinput)
                return True
            else:
                return False
        except:
            return False

    def readPremium(self):
        try:
            strTemp = str(self.strPremium)
            strTemp = strTemp.strip()

            if strTemp.isdigit():
                return int(strTemp)
            else:
                return self.undefined
        except:
            return self._generalError

    def writePremium(self,strinput):

        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if strinput.isdigit():
                self.strPremium = int(strinput)
                return True
            else:
                return False

        except:
            return False

    def readPayout(self):
        try:
            strTemp = str(self.strPayout)
            strTemp = strTemp.strip()

            if strTemp.isdigit():
                return strTemp
            else:
                return self.undefined
        except:
            return self._generalError

    def writePayout(self,strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if strinput.isdigit():
                self.strPayout = int(strinput)
                return True
            else:
                return False

        except:
            return False
class Covers(Constant):
    strCoverCode = ndb.StringProperty()
    strCoverName = ndb.StringProperty()
    strFSPNumber = ndb.StringProperty()
    strCoverType = ndb.StringProperty()



    def readCoverCode(self):
        try:
            strTemp = str(self.strCoverCode)
            strTemp = strTemp.strip()

            if not(strTemp == self.undefined):
                return strTemp
            else:
                return self.undefined
        except:
            return self._generalError

    def writeCoverCode(self, strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()
            strinput = strinput.upper()

            if not (strinput == self.undefined):
                self.strCoverCode = strinput
                return True
            else:
                return False
        except:
            return self._generalError

    def readCoverName(self):
        try:
            strTemp = str(self.strCoverName)
            strTemp = strTemp.strip()

            if not(strTemp == self.undefined):
                return strTemp
            else:
                return self.undefined
        except:
            return self._generalError

    def writeCoverName(self,strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if not(strinput == self.undefined):
                self.strCoverName = strinput
                return True
            else:
                return False
        except:
            return self._generalError

    def readFSPNumber(self):
        try:
            strTemp = str(self.strFSPNumber)
            strTemp = strTemp.strip()

            if not(strTemp == self.undefined):
                return strTemp
            else:
                return self.undefined
        except:
            return self._generalError

    def writeFSPNumber(self,strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if not(strinput == self.undefined):
                self.strFSPNumber = strinput
                return True
            else:
                return False
        except:
            return self._generalError

    def readCoverType(self):
        try:
            strTemp = str(self.strCoverType)
            strTemp = strTemp.strip()

            if not(strTemp == self.undefined):
                return strTemp
            else:
                return self.undefined
        except:
            return self._generalError

    def writeCoverType(self,strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if not(strinput == self.undefined):
                self.strCoverType = strinput
                return True
            else:
                return False

        except:
            return False
class CoversQuote(Constant):

    strSelectedCoverCode = ndb.StringProperty()
    strSelectedPlan = ndb.StringProperty()

    strQuoteNumber = ndb.IntegerProperty()

    strQuoteDate = ndb.DateProperty()
    strQoutedPolicyNumber = ndb.StringProperty()
    strQuoteTotalPremiums = ndb.IntegerProperty()


    def readSelectedCoverCode(self):
        try:
            strTemp = str(self.strSelectedCoverCode)
            strTemp = strTemp.strip()

            if not(strTemp == self.undefined):
                return strTemp
            else:
                return self.undefined
        except:
            return self._generalError
    def writeSelectedCoverCode(self,strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if not(strinput == self.undefined):
                self.strSelectedCoverCode = strinput
                return True
            else:
                return False
        except:
            return False
    def readSelectedPlan(self):
        try:
            strTemp = str(self.strSelectedPlan)
            strTemp = strTemp.strip()

            if not(strTemp == self.undefined):
                return strTemp
            else:
                return self.undefined
        except:
            return self._generalError
    def writeSelectedPlan(self,strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if not(self.strSelectedPlan == self.undefined):
                self.strSelectedPlan = strinput
                return True
            else:
                return False
        except:
            return False
    def readQouteNumber(self):
        try:
            strTemp = str(self.strQuoteNumber)
            strTemp = strTemp.strip()

            if not(strTemp == self.undefined):
                return int(strTemp)
            else:
                return self.undefined
        except:
            return self._generalError
    def writeQuoteNumber(self,strinput):
        try:

            strinput = str(strinput)
            strinput = strinput.strip()

            if not(strinput == self.undefined):
                self.strQuoteNumber = int(strinput)
                return True
            else:
                return False
        except:
            return False
    def readQuoteDate(self):
        try:

            strTemp = str(self.strQuoteDate)
            strTemp = strTemp.strip()

            if not(strTemp == self.undefined):
                return strTemp
            else:
                return self.undefined
        except:
            return self._generalError
    def writeQuoteDate(self,strinput):
        try:
            strinput = str(strinput)
            DateList = strinput.split("-")

            if len(DateList) > 0:
                DateYear = DateList[0]
                DateYear = int(DateYear)
                DateMonth = DateList[1]
                DateMonth = int(DateMonth)
                DateDay = DateList[2]
                DateDay = int(DateDay)

                self.strQuoteDate = datetime(year=DateYear,month=DateMonth,day=DateDay)
                return True
            else:
                return False
        except:
            return False
    def readQuotePolicyNumber(self):
        try:
            strTemp = str(self.strQoutedPolicyNumber)
            strTemp = strTemp.strip()

            if not(strTemp == self.undefined):
                return strTemp
            else:
                return self.undefined
        except:
            return self._generalError
    def writeQuotePolicyNumber(self,strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if not(strinput == self.undefined):
                self.strQoutedPolicyNumber = strinput
                return True
            else:
                return False
        except:
            return False
    def readQuoteTotalPremiums(self):
        try:
            strTemp = str(self.strQuoteTotalPremiums)
            strTemp = strTemp.strip()

            if strTemp.isdigit():
                return int(strTemp)
            else:
                return self.undefined
        except:
            return self._generalError
    def writeQuotedTotalPremiums(self,strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if strinput.isdigit():
                self.strQuoteTotalPremiums = int(strinput)
                return True
            else:
                return False
        except:
            return False

class DynamicEditCoversHandler(webapp2.RequestHandler):
    def get(self):
        Guser = users.get_current_user()

        if Guser:

            logging.info(msg="Edit Covers Dynamic Handler Ran")

            findRequest = Covers.query()
            CoversList = findRequest.fetch()

            template = template_env.get_template('templates/dynamic/covers/editcovers.html')
            Context = {'covers': CoversList}
            self.response.write(template.render(Context))

    def post(self):
        """
            var varstrCoverType = document.getElementById('strCoverType').value;
            var varstrCoverCode = document.getElementById('strCoverCode').value;
            var varstrCoverName = document.getElementById('strCoverName').value;
            var varstrCoverFSP = document.getElementById('strCoverFSP').value;

        :return:
        """
        Guser = users.get_current_user()

        if Guser:

            strCoverType = self.request.get('vstrCoverType')
            logging.info(strCoverType)
            strCoverCode = self.request.get('vstrCoverCode')
            logging.info(strCoverCode)
            strCoverName = self.request.get('vstrCoverName')
            logging.info(strCoverName)
            strCoverFSP = self.request.get('vstrCoverFSP')
            logging.info(strCoverFSP)


            CoverInfo = Covers()

            findRequest = Covers.query(Covers.strCoverCode == strCoverCode)
            CoverFound = findRequest.fetch()


            if len(CoverFound) > 0:

                findRequest = Covers.query()
                CoversList = findRequest.fetch()

                template = template_env.get_template('templates/dynamic/covers/editcovers.html')
                Context = {'covers': CoversList, 'ErrorDiag': "Cannot Add Duplicate Covers"}
                self.response.write(template.render(Context))

            else:

                if CoverInfo.writeCoverCode(strinput=strCoverCode) and CoverInfo.writeFSPNumber(strinput=strCoverFSP):
                    CoverInfo.writeReference(strinput=Guser.user_id())
                    CoverInfo.writeCoverName(strinput=strCoverName)
                    CoverInfo.writeCoverType(strinput=strCoverType)

                    CoverInfo.put()

                    findRequest = Covers.query()
                    CoversList = findRequest.fetch()

                    template = template_env.get_template('templates/dynamic/covers/editcovers.html')
                    Context = {'covers': CoversList}
                    self.response.write(template.render(Context))

                else:
                    findRequest = Covers.query()
                    CoversList = findRequest.fetch()

                    template = template_env.get_template('templates/dynamic/covers/editcovers.html')
                    Context = {'covers': CoversList}
                    self.response.write(template.render(Context))

class RemoveCoversHandler(webapp2.RequestHandler):

    def post(self):

        Guser = users.get_current_user()

        if Guser:

            strCoverCode = self.request.get('vstrCoverCode')

            findRequest = Covers.query(Covers.strCoverCode == strCoverCode)
            RemoveList = findRequest.fetch()



            if len(RemoveList) > 0:
                Remove = RemoveList[0]
                Remove.key.delete()

                template = template_env.get_template('templates/dynamic/covers/removestatus.html')
                Context = {'strCoverCode': strCoverCode}
                self.response.write(template.render(Context))
            else:
                template = template_env.get_template('templates/dynamic/covers/removestatus.html')
                Context = {'ErrorMessage': "Cover Not Found"}
                self.response.write(template.render(Context))

class EditCoversHandler(webapp2.RequestHandler):

    def get(self):
        Guser = users.get_current_user()

        if Guser:
            URL = str(self.request.url)

            URLlist = URL.split("/")

            CoverCode = URLlist[len(URLlist) - 1]
            strCoverCode = str(CoverCode)
            strCoverCode = strCoverCode.upper()

            Cover = Covers()


            findRequest = Covers.query(Covers.strCoverCode == strCoverCode)
            CoverList = findRequest.fetch()

            if len(CoverList) > 0:
                Cover = CoverList[0]

                findRequest = PlanRows.query(PlanRows.strCoverCode == strCoverCode)
                PlanRowsList = findRequest.fetch()



                template = template_env.get_template('templates/dynamic/covers/editthiscover.html')
                Context = {'Cover': Cover, 'PlansList' : PlanRowsList}
                self.response.write(template.render(Context))

    def post(self):
        """
            def writePlanRow(self, strInPlanRowNumber, strinCoverCode, clsinput):
                try:

                    strInPlanRowNumber = str(strInPlanRowNumber)
                    strInPlanRowNumber = strInPlanRowNumber.strip()

                    strinCoverCode = str(strinCoverCode)
                    strinCoverCode = strinCoverCode.strip()

                    if strInPlanRowNumber.isdigit():
                        strInPlanRowNumber = int(strInPlanRowNumber)
                        findRequest = PlanRows.query(PlanRows.strPlanRowNumber == strInPlanRowNumber,
                                                     PlanRows.strCoverCode == strinCoverCode)
                        ThisPlanRowList = findRequest.fetch()

                        if len(ThisPlanRowList) > 0:
                            ThisPlanRow = ThisPlanRowList[0]
                            if len(clsinput) == 7:
                                ThisPlanRow.strPlanRow = clsinput
                                ThisPlanRow.put()
                                return True
                            else:
                                return False

                        else:
                            return False
                    else:
                        return False
                except:
                    return False


        :return:
        """
        pass

class LoadPlanRowsHandler(webapp2.RequestHandler):

    def get(self):

        strCoverCode = self.request.get('vstrCoverCode')

        findRequest = PlanRows.query(PlanRows.strCoverCode == strCoverCode)
        PlanRowsList = findRequest.fetch()



        template = template_env.get_template('templates/dynamic/covers/PlanRowsList.html')
        Context = {'PlansList': PlanRowsList}
        self.response.write(template.render(Context))

    def post(self):
        Guser = users.get_current_user()

        if Guser:

            strCoverCode = self.request.get('vstrCoverCode')
            strRowNumber = self.request.get('vstrRowNumber')
            strColNumber = self.request.get('vstrColNumber')
            strMemberType = self.request.get('vstrMemberType')
            strYearLow = self.request.get('vstrYearLow')
            strYearHigh = self.request.get('vstrYearHigh')
            strPremium = self.request.get('vstrPremium')
            strPayout = self.request.get('vstrPayout')

            Plan = PlanRows()

            Plan.writeReference(strinput=Guser.user_id())
            Plan.writeCoverCode(strinput=strCoverCode)
            Plan.writePlanRowNumber(strinput=strRowNumber)
            Plan.writePlanColNumber(strinput=strColNumber)
            Plan.writeMemberType(strinput=strMemberType)
            Plan.writeYearLow(strinput=strYearLow)
            Plan.writeYearHigh(strinput=strYearHigh)
            Plan.writePremium(strinput=strPremium)
            Plan.writePayout(strinput=strPayout)

            Plan.put()


            findRequest = PlanRows.query(PlanRows.strCoverCode == strCoverCode)
            PlanRowsList = findRequest.fetch()

            template = template_env.get_template('templates/dynamic/covers/PlanRowsList.html')
            Context = {'PlansList': PlanRowsList}
            self.response.write(template.render(Context))

class RemovePlanRowsHandler(webapp2.RequestHandler):

    def get(self):

        strCoverCode = self.request.get('vstrCoverCode')

        logging.info(strCoverCode)

        logging.info(self.request.url)


        findRequest = PlanRows.query(PlanRows.strCoverCode == strCoverCode)
        PlanRowsList = findRequest.fetch()

        for Plans in PlanRowsList:
            Plans.key.delete()

        self.redirect(uri="/dynamic/admin/editcovers/loadplanrows")


    def post(self):

        strCoverCode = self.request.get('vstrCoverCode')
        logging.info(strCoverCode)
        strRemoveCol = self.request.get('vstrRemoveCol')
        logging.info(strRemoveCol)
        strRemoveCol = int(strRemoveCol)
        strRemoveRow = self.request.get('vstrRemoveRow')
        logging.info(strRemoveRow)
        strRemoveRow = int(strRemoveRow)

        findRequest  = PlanRows.query(PlanRows.strCoverCode == strCoverCode , PlanRows.strPLanColNumber == strRemoveCol ,
                                      PlanRows.strPlanRowNumber == strRemoveRow)
        Planlist = findRequest.fetch()

        for Plan in Planlist:
            Plan.key.delete()

        self.redirect(uri="/dynamic/admin/editcovers/loadplanrows")

class CreateQuoteHandler(webapp2.RequestHandler):

    def get(self):

        Guser = users.get_current_user()
        if Guser:

            strPolicyNumber = self.request.get('vstrPolicyNumber')

            findRequest = ClientsPersonalDetails.query(ClientsPersonalDetails.strPolicyNum == strPolicyNumber)
            PolicyHolderList = findRequest.fetch()

            findRequest = Spouses.query(Spouses.strPolicyNum == strPolicyNumber)
            SpousesList = findRequest.fetch()

            findRequest = ChildrenDetails.query(ChildrenDetails.strPolicyNum == strPolicyNumber)
            ChildrenList = findRequest.fetch()


            findRequest = ExtendedFamily.query(ExtendedFamily.strPolicyNum == strPolicyNumber)
            ExtendedList = findRequest.fetch()

            findRequest = Beneficiary.query(Beneficiary.strPolicyNum == strPolicyNumber)
            BeneficiaryList = findRequest.fetch()

            if (len(PolicyHolderList) > 0) and (len(SpousesList) > 0) and (len(ChildrenList) > 0) and (len(ExtendedList) > 0):
                template = template_env.get_template('templates/dynamic/covers/family-extended.html')
                Context = {'strPolicyNum': strPolicyNumber,'PrincipalMemberList': PolicyHolderList,'SpouseList': SpousesList, 'ChildrensList': ChildrenList,
                           'ExtendedList': ExtendedList}
                self.response.write(template.render(Context))
            elif (len(PolicyHolderList) > 0) and (len(ExtendedList) > 0):
                template = template_env.get_template('templates/dynamic/covers/family-extended.html')
                Context = {'strPolicyNum': strPolicyNumber,'PrincipalMemberList': PolicyHolderList,'ExtendedList': ExtendedList}
                self.response.write(template.render(Context))
            elif (len(PolicyHolderList) > 0) and (len(SpousesList) > 0) and (len(ChildrenList) > 0):
                template = template_env.get_template('templates/dynamic/covers/family-quote.html')
                Context = {'strPolicyNum': strPolicyNumber,'PrincipalMemberList': PolicyHolderList, 'SpouseList': SpousesList, 'ChildrensList': ChildrenList}
                self.response.write(template.render(Context))

            elif (len(PolicyHolderList) > 0) and (len(ChildrenList) > 0):
                template = template_env.get_template('templates/dynamic/covers/family-quote.html')
                Context = {'strPolicyNum': strPolicyNumber,'PrincipalMemberList': PolicyHolderList, 'SpouseList': SpousesList, 'ChildrensList': ChildrenList}
                self.response.write(template.render(Context))
            elif (len(PolicyHolderList) > 0) and (len(SpousesList) > 0):
                template = template_env.get_template('templates/dynamic/covers/family-quote.html')
                Context = {'strPolicyNum': strPolicyNumber,'PrincipalMemberList': PolicyHolderList, 'SpouseList': SpousesList, 'ChildrensList': ChildrenList}
                self.response.write(template.render(Context))

            elif (len(PolicyHolderList) > 0):
                template = template_env.get_template('templates/dynamic/covers/single-quote.html')
                Context = {'strPolicyNum': strPolicyNumber,'PrincipalMemberList': PolicyHolderList}
                self.response.write(template.render(Context))











class FuneralCoverPrintHandler(webapp2.RequestHandler):
    def get(self):

        Guser = users.get_current_user()

        if Guser:
            Date = datetime.now()
            Date = Date.date()
            Date = str(Date)

            strPolicyNumber = self.request.get('vstrPolicyNumber')

            findRequest = ExtendedFamily.query(ExtendedFamily.strPolicyNum == strPolicyNumber)

            ExtendedFamilyList = findRequest.fetch()

            strTotalPremiums = self.request.get('vstrTotalPremiums')

            FamilyPremium = int(strTotalPremiums)

            for Extend in ExtendedFamilyList:
                strIDNumber = str(Extend.strIDNumber)
                PlanChoice = str(self.request.get(strIDNumber))

                PlanChoice = int(PlanChoice)
                Extend.writePremium(strinput=PlanChoice)

                FamilyPremium = FamilyPremium - int(PlanChoice)

                for Plans in Extend.strQualifiedPlansList:
                    if int(Plans.strPremium) == int(Extend.readPremium()):
                        Extend.writeBenefit(strinput=Plans.readPayout())


            strFamilyPlanChoice = self.request.get('vstrFamilyPlanChoice')
            strDayFirstPremium = self.request.get('vstrDayFirstPremium')

            CreatePolicy = Policy()

            CreatePolicy.writeReference(strinput=Guser.user_id())
            CreatePolicy.writePolicyNum(strinput=strPolicyNumber)
            CreatePolicy.writeTotalPremiums(strinput=strTotalPremiums)

            CreatePolicy.writeFirstPremiumDate(strinput=strDayFirstPremium)

            #TODO- Make note to save the Attached Policy Documents to the policy

            CreatePolicy.writePaymentCode(strinput=strPolicyNumber)
            CreatePolicy.put()
            WorkPol = WorkingPolicy()

            findRequest = WorkingPolicy.query(WorkingPolicy.strPolicyNum == strPolicyNumber)
            WorkPolList = findRequest.fetch()

            for WorkPol in WorkPolList:
                WorkPol.key.delete()


            FindRequest = EmploymentDetails.query(EmploymentDetails.strReference == Guser.user_id())
            EmployList = FindRequest.fetch()

            if len(EmployList) > 0:
                Employ = EmployList[0]

                strBranchCode = Employ.strBranchCode

                FindRequest = BranchDetails.query(BranchDetails.strCompanyBranchCode == strBranchCode)
                BranchDet = FindRequest.fetch(limit=1)
                BranchDet = BranchDet[0]
                Address = BranchDet.strCompanyBranchAddress
            else:
                Address = ""



            template = template_env.get_template('templates/dynamic/covers/Quote-Print.html')
            context = {'vstrTodayDate': Date, 'Address': Address}
            self.response.write(template.render(context))


class PaymentDetailsHandler(webapp2.RequestHandler):
    def get(self):
        Guser = users.get_current_user()
        if Guser:
            template = template_env.get_template('templates/dynamic/covers/PaymentDetails.html')
            Context = {}
            self.response.write(template.render(Context))
        else:
            pass


class ActivatePolicyHandler(webapp2.RequestHandler):
    def get(self):

        strPolicyNumber = self.request.get('vstrPolicyNumber')
        strPolicyNumber = strPolicyNumber.strip()

        findRequest = ClientsPersonalDetails.query(ClientsPersonalDetails.strPolicyNum == strPolicyNumber)
        PolicyHolderList = findRequest.fetch()

        findRequest = ChildrenDetails.query(ChildrenDetails.strPolicyNum == strPolicyNumber)
        ChildrensList = findRequest.fetch()

        findRequest = Spouses.query(Spouses.strPolicyNum == strPolicyNumber)
        SpousesList = findRequest.fetch()

        findRequest = ExtendedFamily.query(ExtendedFamily.strPolicyNum == strPolicyNumber)
        ExtendedList = findRequest.fetch()

        findRequest = Policy.query(Policy.strPolicyNum == strPolicyNumber)
        thisPolicyList = findRequest.fetch()

        if len(thisPolicyList) > 0:
            thisPolicy = thisPolicyList[0]
        else:
            thisPolicy = Policy()


        if not(thisPolicy.readPlanChoice() == None):
            FamilyPlanChoice = thisPolicy.readPlanChoice()
        else:
            FamilyPlanChoice = None

        if not(thisPolicy.readExtendedPlanChoice() == None):
            ExtendedPlanChoice = thisPolicy.readExtendedPlanChoice()
        else:
            ExtendedPlanChoice = None

        if not(thisPolicy.readSinglePlanChoice() == None):
            SinglePlanChoice = thisPolicy.readSinglePlanChoice()
        else:
            SinglePlanChoice = None


        FamilyCoverAmount = 0

        if FamilyPlanChoice == "A":
            FamilyCoverAmount = 5000
            ChildrenRange = "R 3000.00 -- R 1000.00"
        elif FamilyPlanChoice == "B":
            FamilyCoverAmount = 7000
            ChildrenRange = "R 3500.00 -- R 1000.00"
        elif FamilyPlanChoice == "C":
            FamilyCoverAmount = 10000
            ChildrenRange = "R 5000.00 -- R 1200.00"
        elif FamilyPlanChoice == "D":
            FamilyCoverAmount = 12000
            ChildrenRange = "R 6500.00 -- R 1500.00"
        else:
            ChildrenRange =""


        ExtendedCoverAmount = 0
        if ExtendedPlanChoice == "A":
            ExtendedCoverAmount = 5000
        elif ExtendedPlanChoice == "B":
            ExtendedCoverAmount = 7000
        elif ExtendedPlanChoice == "C":
            ExtendedCoverAmount = 10000
        elif ExtendedPlanChoice == "D":
            ExtendedCoverAmount = 12000

        SingleCoverAmount = 0
        if SinglePlanChoice == "A":
            SingleCoverAmount = 5000
        if SinglePlanChoice == "B":
            SingleCoverAmount = 7000
        if SinglePlanChoice == "C":
            SingleCoverAmount = 10000
        if SinglePlanChoice == "D":
            SingleCoverAmount = 12000

        strTotalPremiums = thisPolicy.readTotalPremiums()

        logging.info("Family Plan Choice : " + FamilyPlanChoice)
        if SingleCoverAmount == 0:
            Context = {'vstrPolicyNumber': strPolicyNumber, 'vstrTotalPremiums': strTotalPremiums, 'ChildCoverRange': ChildrenRange, 'ChildrensList': ChildrensList, 'SpouseList': SpousesList,
                       'ExtendedList': ExtendedList, 'PrincipalMemberList': PolicyHolderList,'PrincipalMemberCoverAmount': FamilyCoverAmount,
                       'SpouseCoverAmount' : FamilyCoverAmount,'ExtendedCoverAmount':ExtendedCoverAmount}
        else:
            Context = {'vstrPolicyNumber': strPolicyNumber, 'vstrTotalPremiums': strTotalPremiums, 'ChildCoverRange': ChildrenRange, 'ChildrensList': ChildrensList, 'SpouseList': SpousesList,
                       'ExtendedList': ExtendedList, 'PrincipalMemberList': PolicyHolderList,'PrincipalMemberCoverAmount': SingleCoverAmount
                       }


        template = template_env.get_template('templates/dynamic/covers/activate.html')
        self.response.write(template.render(Context))


    def post(self):
        strPolicyNumber = self.request.get('vstrPolicyNumber')
        strPolicyNumber = strPolicyNumber.strip()

        findRequest = Policy.query(Policy.strPolicyNum == strPolicyNumber)
        PolicyList = findRequest.fetch()

        if len(PolicyList) > 0:
            thisPolicy = PolicyList[0]

            thisPolicy.writeActivatePolicy(strinput=True)

            thisPolicy.put()
            findRequest = WorkingPolicy.query(WorkingPolicy.strPolicyNum == strPolicyNumber)
            WorkingList = findRequest.fetch()

            if len(WorkingList) > 0:
                WorkingPol = WorkingList[0]
                WorkingPol.writeActivated(strinput=True)
                WorkingPol.put()

            self.response.write("""
            Policy Activated <a href="/employees/funeral-cover" class="btn btn-success btn-block"> Create New Policy </a>
            """)








app = webapp2.WSGIApplication([
    ('/dynamic/admin/editcovers', DynamicEditCoversHandler),
    ('/dynamic/admin/editcovers/remove', RemoveCoversHandler),
    ('/dynamic/admin/editcovers/loadplanrows', LoadPlanRowsHandler),
    ('/dynamic/admin/editcovers/removeplanrows', RemovePlanRowsHandler),
    ('/admin/active-policy/create-quote', CreateQuoteHandler),
    ('/admin/active-policy/payment-details', PaymentDetailsHandler),
    ('/admin/active-policy/activate', ActivatePolicyHandler),
    ('/dynamic/admin/covers/.*', EditCoversHandler),
    ('/employees/funeral-cover/print', FuneralCoverPrintHandler)


], debug=True)





