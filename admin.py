import os
import webapp2
import jinja2
from google.appengine.ext import ndb
from google.appengine.api import users
import logging
template_env = jinja2.Environment(
loader=jinja2.FileSystemLoader(os.getcwd()))

from Employee import *
from database import UserRights
from Contact import ContactMessages
class EmpExistHandler(webapp2.RequestHandler):
    def get(self):
        template =template_env.get_template('templates/dynamic/admin/empexist.html')
        context ={}
        self.response.write(template.render(context))


class DeleteEmployeesHandler(webapp2.RequestHandler):
    def post(self):
        try:
            strEmployeeCode = self.request.get('vstrEmployeeCode')
            logging.info("Employees Delete Executed")
            findRequest = EmploymentDetails.query(EmploymentDetails.strEmployeeCode == strEmployeeCode)
            TempEmployees = findRequest

            strReference = ""

            for Employee in TempEmployees:
                strReference = Employee.strReference
                Employee.key.delete()

            findRequest = ResidentialAddress.query(ResidentialAddress.strEmployeeCode == strEmployeeCode)
            TempPhysical = findRequest

            for physical in TempPhysical:
                physical.key.delete()

            findRequest = PostalAddress.query(PostalAddress.strEmployeeCode == strEmployeeCode)
            TempPostal  = findRequest

            for postal in TempPostal:
                postal.key.delete()

            findRequest = BankingDetails.query(BankingDetails.strEmployeeCode == strEmployeeCode)
            TempBanking = findRequest

            for banking in TempBanking:
                banking.key.delete()

            findRequest = ContactDetails.query(ContactDetails.strEmployeeCode == strEmployeeCode)
            TempContact = findRequest

            for contact in TempContact:
                contact.key.delete()

            findRequest = UserRights.query(UserRights.strReference == strReference)
            RightsList = findRequest.fetch()

            if len(RightsList) > 0:
                Rights = RightsList[0]
                Rights.key.delete()

            logging.info("Complete")
            self.redirect('/admin')
        except:
            logging.info("Error")

class SuspendOnPayHandler(webapp2.RequestHandler):
    def post(self):

        try:

            strEmployee = self.request.get('vstrEmployeeCode')
            findRequest = EmploymentDetails.query(EmploymentDetails.strEmployeeCode == strEmployee)
            TempEmploy = findRequest.fetch()

            for employee in TempEmploy:
                employee.writeSuspendOnPay(strinput=True)
                employee.put()

            self.redirect('/admin')
        except:
            self.redirect('/admin')

    def get(self):
        try:

            strEmployee = self.request.get('vstrEmployeeCode')
            findRequest = EmploymentDetails.query(EmploymentDetails.strEmployeeCode == strEmployee)
            TempEmploy = findRequest.fetch()

            for employee in TempEmploy:
                employee.writeSuspendOnPay(strinput=False)
                employee.put()

            self.redirect('/admin')
        except:
            self.redirect('/admin')

class SuspendHandler(webapp2.RequestHandler):
    def post(self):
        try:

            strEmployeeCode = self.request.get('vstrEmployeeCode')
            findRequest = EmploymentDetails.query(EmploymentDetails.strEmployeeCode == strEmployeeCode)
            TempEmploy = findRequest.fetch()

            for employee in TempEmploy:
                employee.writeSuspend(strinput=True)
                employee.put()

            self.redirect('/admin')
        except:
            self.redirect('/admin')


    def get(self):
        try:

            strEmployeeCode = self.request.get('vstrEmployeeCode')
            findRequest = EmploymentDetails.query(EmploymentDetails.strEmployeeCode == strEmployeeCode)
            TempEmploy = findRequest.fetch()

            for employee in TempEmploy:
                employee.writeSuspend(strinput=False)
                employee.put()

            self.redirect('/admin')
        except:
            self.redirect('/admin')


class TwentyFourHourLockHandler(webapp2.RequestHandler):
    def post(self):
        try:
            strEmployeeCode = self.request.get('vstrEmployeeCode')
            findRequest = EmploymentDetails.query(EmploymentDetails.strEmployeeCode == strEmployeeCode)
            TempEmploy = findRequest.fetch()

            for employee in TempEmploy:
                employee.write24HourLock(strinput=True)
                employee.put()

            self.redirect(('/admin'))
        except:
            self.redirect('/admin')

    def get(self):
        try:
            strEmployeeCode = self.request.get('vstrEmployeeCode')
            findRequest = EmploymentDetails.query(EmploymentDetails.strEmployeeCode == strEmployeeCode)
            TempEmploy = findRequest.fetch()

            for employee in TempEmploy:
                employee.write24HourLock(strinput=False)
                employee.put()

            self.redirect(('/admin'))
        except:
            self.redirect('/admin')



class LockUserIndefinetelyHandler(webapp2.RequestHandler):
    def post(self):
        try:
            strEmployeeCode = self.request.get('vstrEmployeeCode')
            findRequest = EmploymentDetails.query(EmploymentDetails.strEmployeeCode == strEmployeeCode)
            TempEmploy = findRequest

            for employee in TempEmploy:
                employee.writeLockUserIndefinetely(strinput=True)
                employee.put()

            self.redirect('/admin')
        except:
            self.redirect('/admin')


    def get(self):
        try:
            strEmployeeCode = self.request.get('vstrEmployeeCode')
            findRequest = EmploymentDetails.query(EmploymentDetails.strEmployeeCode == strEmployeeCode)
            TempEmploy = findRequest

            for employee in TempEmploy:
                employee.writeLockUserIndefinetely(strinput=False)
                employee.put()

            self.redirect('/admin')
        except:
            self.redirect('/admin')



class DynamicBranchEmployeesHandler(webapp2.RequestHandler):
    def get(self):
        Guser = users.get_current_user()

        if Guser:
            URL = str(self.request.url)

            URLList = URL.split("/")

            strBranchCode = URLList[len(URLList) - 1]

            if "#" in strBranchCode:
                strBranchCode = strBranchCode.strip('#')


            findRequest = EmploymentDetails.query(EmploymentDetails.strBranchCode == strBranchCode)
            TempEmploymentList = findRequest.fetch()
            context = {'strCallingURL': URL}
            if len(TempEmploymentList) > 0:
                context = {'employees': TempEmploymentList,'vstrBranchName':"Thohoyandou",
                           'strCallingURL': URL}

            template = template_env.get_template('templates/dynamic/admin/branchemployeelist.html')
            self.response.write(template.render(context))
        else:
            pass

class EmployeeRegistrationRequestHandler(webapp2.RequestHandler):
    def post(self):

        Guser = users.get_current_user()

        if Guser:

            strRegistrationEmail = self.request.get('vstrReqForEmployeeRegister')
            strReference = self.request.get('vstrReqReference')
            strIDNumber = self.request.get('vstrIDNumber')

            EmployeeRequest =  EmployeeRegRequest()

            findRequest = EmployeeRegRequest.query(EmployeeRegRequest.strEmail == Guser.email())
            RequestsLists = findRequest.fetch()

            if len(RequestsLists) > 0:
                pass
            else:
                EmployeeRequest.writeEmail(strinput=Guser.email())
                EmployeeRequest.writeReference(strinput=Guser.user_id())
                EmployeeRequest.writeIDNumber(strinput=strIDNumber)

                EmployeeRequest.put()
        else:
            pass
        self.redirect('/employees')



class UserRightsHandler(webapp2.RequestHandler):

    def get(self):
        Guser = users.get_current_user()
        if Guser:

            findRequest = EmployeeRegRequest.query()
            usersList = findRequest.fetch()

            template = template_env.get_template('templates/dynamic/admin/userrights.html')
            context = {'users': usersList}
            self.response.write(template.render(context))


class AllUserRightsHandler(webapp2.RequestHandler):
    def get(self):
        Guser = users.get_current_user()
        logging.info(msg=" User Rights Called")

        if Guser:
            findRequest = BranchDetails.query()
            branchList = findRequest.fetch()

            URLList = str(self.request.url)

            URLList = URLList.split("/")

            strReference = URLList[len(URLList) - 1]

            findRequest = EmploymentDetails.query(EmploymentDetails.strReference == strReference)
            ThisEmployeeList = findRequest.fetch()

            ThisEmployee = EmploymentDetails()

            if len(ThisEmployeeList) > 0:
                ThisEmployee = ThisEmployeeList[0]
                strUsername = ThisEmployee.readSurname()
                strReference = ThisEmployee.readReference()
                strIDNumber = ThisEmployee.readIDNumber()
                strEmployeeBranch = ThisEmployee.readBranchWorking()
                strFirstname = ThisEmployee.readNames()
                strSurname = ThisEmployee.readSurname()
                strEmployeeCode = ThisEmployee.readEmployeeCode()

                ThisUserRights = UserRights()

                findRequest = UserRights.query(UserRights.strReference == strReference)
                ThisUserRightsList = findRequest.fetch()
                if len(ThisUserRightsList) > 0:
                    ThisUserRights = ThisUserRightsList[0]


                if ThisUserRights.bolIsEmployee:
                    vstrIsEmployee = "YES"
                else:
                    vstrIsEmployee = "NO"

                if ThisUserRights.bolAccessToEmployeesAdminForm:
                    vstrAccessEmployeeAdmin = "YES"
                else:
                    vstrAccessEmployeeAdmin = "NO"

                if ThisUserRights.bolEmployeesFuneralCoverFormReadAccess:
                    vstrSearchCoverPolicy = "YES"
                else:
                    vstrSearchCoverPolicy = "NO"

                if ThisUserRights.bolEmployeesFuneralCoverFormWriteAccess:
                    vstrEditCoverPolicy = "YES"
                else:
                    vstrEditCoverPolicy = "NO"


                if ThisUserRights.bolEmployeesFuneralServicesFormReadAccess:
                    vstrSearchFuneralService = "YES"
                else:
                    vstrSearchFuneralService = "NO"

                if ThisUserRights.bolEmployeesFuneralServicesFormWriteAccess:
                    vstrEditFuneralServices = "YES"
                else:
                    vstrEditFuneralServices = "NO"

                if ThisUserRights.bolEmployeesLeadsFormReadAccess:
                    vstrSearchLeadsForm = "YES"
                else:
                    vstrSearchLeadsForm = "NO"
                if ThisUserRights.bolEmployeesLeadsFormWriteAccess:
                    vstrEditLeadsForm = "YES"
                else:
                    vstrEditLeadsForm = "NO"

                ThisUserRights.writeEmployeeCode(strinput=strEmployeeCode)
                ThisUserRights.writeReference(strinput=strReference)
                ThisUserRights.put()

                template = template_env.get_template('templates/dynamic/admin/thisuserights.html')
                context = {'vstrUsername':strUsername,'vstrReference': strReference, 'vstrIDNumber': strIDNumber,
                           'branches': branchList,'vstrEmployeeBranch': strEmployeeBranch,'vstrEmployeeCode':strEmployeeCode,  'vstrFirstnames': strFirstname,
                           'vstrSurname': strSurname,'vstrIsEmployee': vstrIsEmployee,'vstrAccessEmployeeAdmin':vstrAccessEmployeeAdmin,
                           'vstrSearchCoverPolicy':vstrSearchCoverPolicy,'vstrEditCoverPolicy':vstrEditCoverPolicy,'vstrSearchFuneralService':vstrSearchFuneralService,
                               'vstrEditFuneralServices':vstrEditFuneralServices,'vstrSearchLeadsForm':vstrSearchLeadsForm,
                               'vstrEditLeadsForm':vstrEditLeadsForm}
                self.response.write(template.render(context))

            else:

                findRequest = EmployeeRegRequest.query(EmployeeRegRequest.strReference == strReference)
                EmployeeList = findRequest.fetch()

                EmployeeReq = EmployeeRegRequest()

                if len(EmployeeList) > 0:
                    EmployeeReq = EmployeeList[0]
                    strUsername = EmployeeReq.readEmail()
                    strReference = EmployeeReq.readReference()
                    strIDNumber = EmployeeReq.readIDNumber()
                    strFirstname = ""
                    strSurname = ""
                    strEmployeeBranch = ""


                    findRequest = EmploymentDetails.query()
                    EmployeeListed = findRequest.fetch()

                    NextCode = len(EmployeeListed)
                    NextCode = "E" + str(NextCode)
                    strEmployeeCode = NextCode

                    CodeList = []
                    CodeList.append(NextCode)
                    template = template_env.get_template('templates/dynamic/admin/thisuserights.html')
                    context = {'vstrUsername':strUsername,'vstrReference': strReference, 'vstrIDNumber': strIDNumber,
                               'branches': branchList,'vstrEmployeeBranch': strEmployeeBranch, 'vstrEmployeeCode':strEmployeeCode,
                               'vstrFirstnames': strFirstname,
                               'vstrSurname': strSurname}
                    self.response.write(template.render(context))

                else:
                    pass







        else:
            pass

    def post(self):
        logging.info("saving user rights and settings")

        strIsEmployee = self.request.get('vstrIsEmployee')

        strAccessEmployeeAdmin = self.request.get('vstrAccessEmployeeAdmin')
        strSearchCoverPolicy = self.request.get('vstrSearchCoverPolicy')
        strEditCoverPolicy = self.request.get('vstrEditCoverPolicy')
        strSearchFuneralService = self.request.get('vstrSearchFuneralService')
        strEditFuneralServices = self.request.get('vstrEditFuneralServices')
        strSearchLeadsForm = self.request.get('vstrSearchLeadsForm')
        strEditLeadsForm  = self.request.get('vstrEditLeadsForm')

        Rights = UserRights()
        logging.info(msg=strIsEmployee)

        URL = str(self.request.url)
        URLList = URL.split("/")
        strReference = URLList[len(URLList)-1]


        findRequest = UserRights.query(UserRights.strReference == strReference)
        RightsList = findRequest.fetch()

        if len(RightsList) > 0:
            Rights = RightsList[0]

        if strIsEmployee == "YES":
            Rights.setEmployeeUserRights()
            logging.info(msg="Is employee")

        if strAccessEmployeeAdmin == "YES":
            Rights.bolEmployeesAdminFormReadAccess = True
        else:
            Rights.bolEmployeesAdminFormReadAccess = False

        if strSearchCoverPolicy == "YES":
            Rights.bolEmployeesFuneralCoverFormReadAccess =True
        else:
            Rights.bolEmployeesFuneralCoverFormReadAccess = False

        if strEditCoverPolicy == "YES":
            Rights.bolEmployeesFuneralCoverFormWriteAccess = True
        else:
            Rights.bolEmployeesFuneralCoverFormWriteAccess = False

        if strSearchFuneralService == "YES":
            Rights.bolEmployeesFuneralServicesFormReadAccess = True
        else:
            Rights.bolEmployeesFuneralServicesFormReadAccess = False

        if strEditFuneralServices == "YES":
            Rights.bolEmployeesFuneralServicesFormWriteAccess = True
        else:
            Rights.bolEmployeesFuneralServicesFormWriteAccess = False

        if strSearchLeadsForm == "YES":
            Rights.bolEmployeesLeadsFormReadAccess = True
        else:
            Rights.bolEmployeesLeadsFormReadAccess = False

        if strEditLeadsForm == "YES":
            Rights.bolEmployeesLeadsFormWriteAccess = True
        else:
            Rights.bolEmployeesLeadsFormWriteAccess = False

        URL = str(self.request.url)
        URLlist = URL.split("/")

        strReference = URLlist[len(URLlist) - 1]

        Rights.writeReference(strinput=strReference)

        Rights.put()


        template = template_env.get_template('templates/dynamic/admin/rightsresponse.html')
        context = {'vstrIsEmployee': strIsEmployee,'vstrAccessEmployeeAdmin': strAccessEmployeeAdmin, 'vstrSearchCoverPolicy': strSearchCoverPolicy,
                   'vstrEditCoverPolicy': strEditCoverPolicy, 'vstrSearchFuneralService': strSearchFuneralService,
                   'vstrEditFuneralServices': strEditFuneralServices, 'vstrSearchLeadsForm': strSearchLeadsForm,
                   'vstrEditLeadsForm': strEditLeadsForm}
        self.response.write(template.render(context))


class UserPersonalsHandler(webapp2.RequestHandler):
    def post(self):
        Guser = users.get_current_user()

        if Guser:
            strFirstnames = self.request.get('vstrFirstnames')
            strSurname = self.request.get('vstrSurname')
            strIDNumber = self.request.get('vstrIDNumber')
            strEmployeeCode = self.request.get('vstrEmployeeCode')
            strBranchCode = self.request.get('vstrBranchCode')

            URL = str(self.request.url)

            URLList = URL.split("/")
            strReference = URLList[len(URLList) - 1]

            findRequest = EmploymentDetails.query(EmploymentDetails.strReference == strReference)
            EmployeeList = findRequest.fetch()

            Employee = EmploymentDetails()

            if len(EmployeeList) > 0:
                Employee = EmployeeList[0]
            else:
                pass

            Employee.writeReference(strinput=strReference)
            Employee.writeEmployeeCode(strinput=strEmployeeCode)
            Employee.writeBranchWorking(strinput=strBranchCode)
            Employee.writeIDNumber(strinput=strIDNumber)
            Employee.writeSurname(strinput=strSurname)
            Employee.writeNames(strinput=strFirstnames)

            Employee.put()

            FindRequest = EmployeeRegRequest.query(EmployeeRegRequest.strReference == strReference)
            EmployeeReqList = FindRequest.fetch()

            findRequest = UserRights.query(UserRights.strReference == strReference)
            UserRightsList =findRequest.fetch()
            UserRight = UserRights()

            if len(UserRightsList) > 0:
                UserRight = UserRightsList[0]

            UserRight.writeReference(strinput=strReference)
            UserRight.writeEmployeeCode(strinput=strEmployeeCode)
            UserRight.put()


            if len(EmployeeReqList) > 0:
                EmployeeReq = EmployeeReqList[0]
                try:
                    EmployeeReq.key.delete()
                except:
                    pass
            else:
                pass


            template = template_env.get_template('templates/dynamic/admin/personalsresponse.html')
            context = {'vstrFirstnames': strFirstnames, 'vstrSurname': strSurname,'vstrIDNumber':strIDNumber,
                       'vstrEmployeeCode': strEmployeeCode,'vstrReference': strReference,'vstrBranchCode':strBranchCode}

            self.response.write(template.render(context))


class ContactFormMessagesHandler(webapp2.RequestHandler):
    def get(self):
        Guser = users.get_current_user()
        if Guser:
            findRequest = ContactMessages.query(ContactMessages.strResponseSent == False)
            ContactMessagesList = findRequest.fetch()
            TotalMessages = len(ContactMessagesList)
            Context = {'ContactMessagesList': ContactMessagesList, 'TotalMessages': TotalMessages}
            template = template_env.get_template('templates/dynamic/contact/inbox.html')
            self.response.write(template.render(Context))
        else:
            pass

class ContactFormReadMessageHandler(webapp2.RequestHandler):

    def get(self):
        try:
            URL = self.request.url
            URLlist = URL.split("/")
            MessageReference = URLlist[len(URLlist) - 1]
            MessageReference = str(MessageReference)
            MessageReference = MessageReference.strip()

            findRequest = ContactMessages.query(ContactMessages.strMessageReference == MessageReference)
            ContactMessageList = findRequest.fetch()

            findRequest = ContactMessages.query()
            TotalMessagesList = findRequest.fetch()
            TotalMessages = len(TotalMessagesList)

            ContactMessage = ContactMessageList[0]
            template = template_env.get_template('templates/dynamic/contact/readinbox.html')
            Context = {'ContactMessage': ContactMessage,'TotalMessages': TotalMessages}
            self.response.write(template.render(Context))

        except:
            pass


class BranchFinanceHandler (webapp2.RequestHandler):
    def get(self):
        self.response.write("Updating....")

class FuneralCover24hFormLockHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Placing a 24 hour Lock on Funeral Cover Form')


class FuneralCover12hFormLockHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Placing a 12 Hour Lock on Funeral Cover Form')

class FuneralFormIndefiniteLockHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write("Placing an Indefinite Lock on the Funeral Form <br>")
        vstrEmployeeCode = self.request.get('vstrEmployeeCode')
        logging.info(vstrEmployeeCode)
        self.response.write("For Employee : " + vstrEmployeeCode + "<br>")

        findRequest = UserRights.query(UserRights.strEmployeeCode == vstrEmployeeCode)
        EmployeeRightsList = findRequest.fetch()

        if len(EmployeeRightsList) > 0:
            EmployeeRights = EmployeeRightsList[0]
            EmployeeRights.bolEmployeesFuneralCoverFormWriteAccess = False
            EmployeeRights.put()
            self.response.write("Funeral Cover Edit Access Revoked Indefinitely")
        else:
            self.response.write("Failed to Revoke Edit Access to Funeral Cover Form")



class FuneralFormRemoveAllLocks(webapp2.RequestHandler):
    def get(self):
        self.response.write("Remove All Funeral Cover Locks<br>")
        vstrEmployeeCode = self.request.get('vstrEmployeeCode')
        vstrEmployeeCode = str(vstrEmployeeCode)
        vstrEmployeeCode = vstrEmployeeCode.strip()

        findRequest = UserRights.query(UserRights.strEmployeeCode == vstrEmployeeCode)
        EmployeeRightsList = findRequest.fetch()

        if len(EmployeeRightsList) > 0:
            EmployeeRights = EmployeeRightsList[0]
            EmployeeRights.bolEmployeesFuneralCoverFormWriteAccess = True
            EmployeeRights.put()
            self.response.write("Funeral Cover Edit Access Restored")
        else:
            self.response.write("Failed to Restore Edit Access to Funeral Cover Form")

app = webapp2.WSGIApplication([
    ('/admin/empexist',EmpExistHandler),
    ('/admin/employees/delete',DeleteEmployeesHandler),
    ('/admin/employees/suspendonpay', SuspendOnPayHandler),
    ('/admin/employees/suspend', SuspendHandler),
    ('/admin/employees/24hourlock', TwentyFourHourLockHandler),
    ('/admin/employees/locksystem', LockUserIndefinetelyHandler),
    ('/admin/employees/24hcoverlocks', FuneralCover24hFormLockHandler),
    ('/admin/employees/12hcoverlocks', FuneralCover12hFormLockHandler),
    ('/admin/employees/indefiniteFuneralCoverLock', FuneralFormIndefiniteLockHandler),
    ('/admin/employees/removeAllFuneralFormLocks', FuneralFormRemoveAllLocks),
    ('/dynamic/admin/branch/employees/.*', DynamicBranchEmployeesHandler),

    ('/admin/registration/request', EmployeeRegistrationRequestHandler),
    ('/dynamic/admin/userrights', UserRightsHandler),
    ('/admin/contactform', ContactFormMessagesHandler),
    ('/admin/contact/.*', ContactFormReadMessageHandler),
    ('/admin/financial/branch', BranchFinanceHandler),
    ('/admin/userrights/employees/.*', AllUserRightsHandler),
    ('/admin/userpersonals/employees/.*', UserPersonalsHandler),



], debug=True)

