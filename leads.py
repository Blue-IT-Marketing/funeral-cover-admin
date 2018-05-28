

import os
import webapp2
import jinja2
from google.appengine.ext import ndb
from google.appengine.api import users
import logging
import datetime
template_env = jinja2.Environment(
loader=jinja2.FileSystemLoader(os.getcwd()))

from Employee import EmploymentDetails



class Leads(ndb.Expando):
    strEmployeeCode = ndb.StringProperty()
    strLeadDate = ndb.DateProperty(auto_now_add=True)
    strLeadNotes = ndb.StringProperty()
    strInterestedinFuneralCover = ndb.BooleanProperty(default=False)
    strInterestedinFuneralService = ndb.BooleanProperty(default=False)

    strConversionDate = ndb.DateProperty()
    strConvertedBy = ndb.StringProperty() # Employee Code of the Employee who made the conversion

    strTitle = ndb.StringProperty()
    strFullNames = ndb.StringProperty()
    strSurname = ndb.StringProperty()
    strIDNumber = ndb.StringProperty()

    strDateOfBirth = ndb.StringProperty()
    strResidential = ndb.StringProperty()
    strTownCity = ndb.StringProperty()
    strCountry = ndb.StringProperty()
    strProvince = ndb.StringProperty()
    strPostalCode = ndb.StringProperty()

    strTel = ndb.StringProperty()
    strCell = ndb.StringProperty()
    strEmail = ndb.StringProperty()


    strLeadInterests = ndb.StringProperty() # Funeral Cover or Funeral Service or Other


    def readEmployeeCode(self):
        try:
            strTemp = str(self.strEmployeeCode)
            strTemp = strTemp.strip()

            if not (strTemp == None):
                return strTemp
            else:
                return ""
        except:
            return ""
    def writeEmployeeCode(self,strinput):
        try:

            strinput = str(strinput)
            strinput = strinput.strip()

            if not (strinput == None):
                self.strEmployeeCode = strinput
                return True
            else:
                return False
        except:
            return False
    def readLeadDate(self):
        try:
            return str(self.strLeadDate)
        except:
            return ""
    def readLeadNotes(self):
        try:
            strTemp = str(self.strLeadNotes)
            return strTemp
        except:
            return ""
    def writeLeadNotes(self,strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()
            if not(strinput == None):
                self.strLeadNotes = strinput
                return True
            else:
                return False
        except:
            return False
    def leadInterestedinFuneralCover(self):
        try:
            self.strInterestedinFuneralCover = True

            return True
        except:
            return False
    def leadInterestedinFuneralService(self):
        try:
            self.strInterestedinFuneralService = True
            return True
        except:
            return False
    def readIfInterestedInFuneralCover(self):
        try:
            if self.strInterestedinFuneralCover:
                return "Yes"
            else:
                return "No"
        except:
            return "No"
    def readIfInterestedInFuneralService(self):
        try:
            if self.strInterestedinFuneralService:
                return "Yes"
            else:
                return "No"

        except:
            return "No"
    def readConversionDate(self):
        try:
            strTemp = str(self.strConversionDate)

            return strTemp
        except:
            return ""
    def setConversionDate(self,strinput):
        try:
            thisDate = datetime.datetime.now()
            thisDate = thisDate.date()

            self.strConversionDate = thisDate
            return True
        except:
            return True
    def readConvertedBy(self):
        try:
            strTemp = str(self.strConvertedBy)
            return strTemp
        except:
            return ""
    def writeConvertedBy(self,strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if not(strinput == None):
                self.strConvertedBy = strinput
                return True
            else:
                return False

        except:
            return False
    def readTitle(self):
        try:
            strtemp = str(self.strTitle)
            strtemp = strtemp.strip()

            if not (strtemp == None):
                return strtemp
            else:
                return ""

        except:
            return ""
    def writeTitle(self, strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if not (strinput == None):
                self.strTitle = strinput
                return True
            else:
                return False
        except:
            return False
    def writeNames(self, strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if not (strinput == None):
                self.strFullNames = strinput
                return True
            else:
                return False
        except:
            return False
    def readNames(self):
        try:
            strTemp = str(self.strFullNames)
            strTemp = strTemp.strip()

            if not (strTemp == None):
                return strTemp
            else:
                return ""
        except:
            return ""
    def readSurname(self):
        try:
            strTemp = str(self.strSurname)
            strTemp = strTemp.strip()

            if not (strTemp == None):
                return strTemp
            else:
                return ""
        except:
            return ""
    def writeSurname(self, strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if not (strinput == None):
                self.strSurname = strinput
                return True
            else:
                return False
        except:
            return False
    def readIDNumber(self):
        try:
            strTemp = str(self.strIDNumber)


            if strTemp.isdigit():
                return strTemp
            else:
                return ""
        except:
            return ""
    def writeIDNumber(self, strinput):
        try:
            strinput = str(strinput)


            if strinput.isdigit():
                self.strIDNumber = strinput
                return True
            else:
                return False
        except:
            return False
    def readDateOfBirth(self):
        try:
            strtemp = str(self.strDateOfBirth)
            return strtemp
        except:
            return ""
    def writeDateOfBirth(self, strinput):
        """
            format yyyy-mm-dd
        """
        try:
            strinput = str(strinput)

            Datefields = strinput.split("-")
            if len(Datefields) == 3:
                tempDate = datetime.date(year=int(Datefields[0]), month=int(Datefields[1]), day=int(Datefields[2]))
                self.strDateOfBirth = tempDate
                return True
            else:
                return False
        except:
            return False
    def readResAddress(self):
        try:
            strTemp = str(self.strResidential)
            

            if not (strTemp == None):
                return strTemp
            else:
                return ""
        except:
            return ""
    def writeResAddress(self, strinput):
        try:
            strinput = str(strinput)
            

            if not (strinput == None):
                self.strResidential = strinput
                return True
            else:
                return False
        except:
            return False
    def readCityTown(self):
        try:
            strTemp = str(self.strTownCity)
            strTemp = strTemp.strip()

            if not (strTemp == None):
                return strTemp
            else:
                return ""
        except:
            return ""
    def writeCityTown(self, strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if not (strinput == None):
                self.strTownCity = strinput
                return True
            else:
                return False
        except:
            return False
    def readCountry(self):
        try:
            strTemp = str(self.strCountry)
            strTemp = strTemp.strip()

            if not (strTemp == None):
                return strTemp
            else:
                return ""
        except:
            return ""
    def writeCountry(self, strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if not (strinput == None):
                self.strCountry = strinput
                return True
            else:
                return False
        except:
            return False
    def readProvince(self):
        try:
            strTemp = str(self.strProvince)
            strTemp = strTemp.strip()

            if not (strTemp == None):
                return strTemp
            else:
                return ""
        except:
            return ""
    def writeProvince(self, strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if not (strinput == None):
                self.strProvince = strinput
                return True
            else:
                return False
        except:
            return False
    def readPostalCode(self):
        try:
            strTemp = str(self.strPostalCode)
            strTemp = strTemp.strip()

            if not (strTemp == None):
                return strTemp
            else:
                return ""
        except:
            return ""
    def writePostalCode(self, strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if not (strinput == None):
                self.strPostalCode = strinput
                return True
            else:
                return False
        except:
            return False
    def readCell(self):
        try:
            strTemp = str(self.strCell)
            strTemp = strTemp.strip()

            if not (strTemp == None):
                return strTemp
            else:
                return ""
        except:
            return ""
    def writeCell(self, strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if not (strinput == None):
                self.strCell = strinput
                return True
            else:
                return False
        except:
            return False
    def readTell(self):
        try:
            strTemp = str(self.strTel)
            strTemp = strTemp.strip()

            if not (strTemp == None):
                return strTemp
            else:
                return ""
        except:
            return ""
    def writeTel(self, strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if not (strinput == None):
                self.strTel = strinput
                return True
            else:
                return False
        except:
            return False
    def readEmail(self):
        try:
            strTemp = str(self.strEmail)
            strTemp = strTemp.strip()

            if not (strTemp == None):
                return strTemp
            else:
                return ""
        except:
            return ""
    def writeEmail(self, strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if not (strinput == None):
                self.strEmail = strinput
                return True
            else:
                return False
        except:
            return False
    def readLeadInterests(self):
        try:
            strTemp =str(self.strLeadInterests)
            return strTemp
        except:
            return ""

    def writeLeadInterests(self,strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip().lower()
            if strinput == "funeral service":
                self.leadInterestedinFuneralService()
                self.strLeadInterests = strinput
                return True
            elif strinput == "funeral cover":
                self.leadInterestedinFuneralCover()
                self.strLeadInterests = strinput
                return True
            elif strinput == "other":
                self.strLeadInterests = "other"
                return True
            else:
                return False
        except:
            return False

class LeadResponses(ndb.Expando):
    strReference = ndb.StringProperty() # Reference of the User Using the System at the time
    strEmployeeName = ndb.StringProperty()
    strEmployeeSurname = ndb.StringProperty()
    strEmployeeCode = ndb.StringProperty()
    strIDNumber = ndb.StringProperty() # ID Number of the Lead
    strResponse = ndb.StringProperty()
    strStatus = ndb.StringProperty()
    strDateTimeResponse = ndb.DateTimeProperty(auto_now_add=True)
    strNextSchedule = ndb.DateTimeProperty()

    def readReference(self):
        try:
            strTemp = str(self.strReference)
            return strTemp
        except:
            return None

    def writeReference(self,strinput):
        try:
            strinput = str(strinput)
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
            if strinput.isdigit() and (len(strinput) == 13):
                self.strIDNumber = strinput
                return True
            else:
                return False
        except:
            return False

    def writeResponses(self,strinput):
        try:
            strinput = str(strinput)
            if not(strinput == None):
                self.strResponse = strinput
                return True
            else:
                return False

        except:
            return False

    def writeStatus(self,strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.lower()

            if (strinput == "calllater") or (strinput == "unreachable") or (strinput == "dontcall"):
                self.strStatus = strinput
                return True
            else:
                return False
        except:
            return False

    def writeNextSchedule(self,strinput):
        try:

            if not(strinput == None):
                self.strNextSchedule = strinput
                return True
            else:
                return False
        except:
            return False

class CaptureLeadshandler(webapp2.RequestHandler):
    def get(self):
        Guser = users.get_current_user()
        if Guser:
            vstrTitle = self.request.get('vstrTitle')
            logging.info(vstrTitle)
            vstrSurname = self.request.get('vstrSurname')
            vstrFullnames = self.request.get('vstrFullnames')
            vstrIDNumber = self.request.get('vstrIDNumber')
            vstrDateofBirth = self.request.get('vstrDateofBirth')
            vstrResidential = self.request.get('vstrResidential')
            vstrTownCity = self.request.get('vstrTownCity')
            logging.info(vstrTownCity)
            vstrCountry = self.request.get('vstrCountry')
            vstrProvince = self.request.get('vstrProvince')
            vstrPostalCode = self.request.get('vstrPostalCode')
            vstrTel = self.request.get('vstrTel')
            vstrCell = self.request.get('vstrCell')
            logging.info(vstrCell)
            vstrEmail = self.request.get('vstrEmail')
            vstrLeadNotes = self.request.get('vstrLeadNotes')
            vstrInterest = self.request.get('vstrInterest')

            findRequests = Leads.query(Leads.strIDNumber == vstrIDNumber)
            DuplicateLists = findRequests.fetch()

            if len(DuplicateLists) > 0:
                self.response.write("Lead has already been Captured")
            else:
                try:

                    thisLead = Leads()
                    logging.info("We have SUCCESFULLY CREATED LEAD CAPTURE CLASS")
                    thisLead.writeTitle(strinput=vstrTitle)
                    logging.info("Title Written")
                    thisLead.writeSurname(strinput=vstrSurname)
                    thisLead.writeNames(strinput=vstrFullnames)
                    thisLead.writeIDNumber(strinput=vstrIDNumber)
                    thisLead.writeDateOfBirth(strinput=vstrDateofBirth)
                    thisLead.writeResAddress(strinput=vstrResidential)
                    thisLead.writeCityTown(strinput=vstrTownCity)
                    thisLead.writeCountry(strinput=vstrCountry)
                    logging.info("Till Country")
                    thisLead.writeProvince(strinput=vstrProvince)
                    thisLead.writePostalCode(strinput=vstrPostalCode)
                    thisLead.writeTel(strinput=vstrTel)
                    thisLead.writeCell(strinput=vstrCell)
                    thisLead.writeEmail(strinput=vstrEmail)
                    logging.info("Till Email")

                    thisLead.writeLeadNotes(strinput=vstrLeadNotes)
                    thisLead.writeLeadInterests(strinput=vstrInterest)

                    findRequests = EmploymentDetails.query(EmploymentDetails.strReference == Guser.user_id())
                    EmployeeList = findRequests.fetch()

                    if len(EmployeeList) > 0:
                        Employee = EmployeeList[0]
                        thisLead.writeEmployeeCode(strinput=Employee.strEmployeeCode)
                        thisLead.put()
                        self.response.write("Lead Capture Succesfully")
                    else:
                        self.response.write("Not Authorised to Capture Lead")
                except:
                    self.response.write("An Error Occured Capturing Lead")

        else:
            self.response.write("You are presently not logged in")


class SubLeadHandler(webapp2.RequestHandler):
    def get(self):

        URL = self.request.url
        URL = str(URL)
        vstrRefreshButtonURL = URL
        URLlist = URL.split("/")
        strIDNumber = URLlist[len(URLlist) - 1]

        findRequest = Leads.query(Leads.strIDNumber == strIDNumber)
        LeadList = findRequest.fetch()
        thisLead = Leads()
        if len(LeadList) > 0:
            thisLead = LeadList[0]

        findRequest = Leads.query()
        LeadList = findRequest.fetch()

        findRequest = LeadResponses.query(LeadResponses.strIDNumber == strIDNumber)
        LeadResponseList = findRequest.fetch()

        findRequest = EmploymentDetails.query(EmploymentDetails.strEmployeeCode == thisLead.strEmployeeCode)
        EmployeeList = findRequest.fetch()
        Employee = EmploymentDetails()
        if len(EmployeeList) > 0:
            Employee = EmployeeList[0]


        template = template_env.get_template('templates/dynamic/leads/sublead.html')
        context = {'thisLead':thisLead,'LeadList':LeadList,'vstrRefreshButtonURL': vstrRefreshButtonURL,'Employee':Employee,
                   'LeadResponses': LeadResponseList}
        self.response.write(template.render(context))


class LeadResponseHandler(webapp2.RequestHandler):
    def get(self):
        try:
            Guser = users.get_current_user()
            if Guser:
                vstrLeadResponse = self.request.get('vstrLeadResponse')
                vstrFollowUpStatus = self.request.get('vstrFollowUpStatus')
                vstrNextScheduleCall = self.request.get('vstrNextScheduleCall')
                vstrLeadIDNumber = self.request.get('vstrLeadIDNumber')

                thisLeadResponse = LeadResponses()



                thisLeadResponse.writeReference(strinput=Guser.user_id())

                findRequest = EmploymentDetails.query(EmploymentDetails.strReference == Guser.user_id())
                EmployeeList = findRequest.fetch()

                Employee = EmploymentDetails()
                if len(EmployeeList) > 0:
                    Employee = EmployeeList[0]

                thisLeadResponse.strEmployeeName = Employee.strFullNames
                thisLeadResponse.strEmployeeSurname = Employee.strSurname
                thisLeadResponse.strEmployeeCode = Employee.strEmployeeCode
                thisLeadResponse.writeIDNumber(strinput=vstrLeadIDNumber)
                thisLeadResponse.writeResponses(strinput=vstrLeadResponse)
                thisLeadResponse.writeStatus(strinput=vstrFollowUpStatus)
                thisLeadResponse.writeNextSchedule(strinput=vstrNextScheduleCall)
                thisLeadResponse.put()

                self.response.write("Succesfully saved a lead Response")
            else:
                self.response.write("Failure Saving Lead Response")
        except:
            self.response.write("Fatal Error Saving Lead Response")


class LeadSendEmailHandler(webapp2.RequestHandler):
    def get(self):
        pass

app = webapp2.WSGIApplication([
    ('/leads/capture', CaptureLeadshandler),
    ('/leads/sublead/.*',SubLeadHandler),
    ('/leads/response', LeadResponseHandler),
    ('/leads/sendemail', LeadSendEmailHandler)


], debug=True)

