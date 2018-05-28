#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import os
import webapp2
import jinja2
from google.appengine.ext import ndb
from google.appengine.api import users
import logging
template_env = jinja2.Environment(
loader=jinja2.FileSystemLoader(os.getcwd()))
from database import *
from leads import Leads
class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = template_env.get_template('templates/index.html')
        context = {}
        self.response.write(template.render(context))

class ServicesHandler(webapp2.RequestHandler):
    def get(self):
        template = template_env.get_template('templates/services.html')
        context = {}
        self.response.write(template.render(context))

class EmployeesHandler(webapp2.RequestHandler):
    def get(self):

        Guser = users.get_current_user()

        if Guser:
            strReference = Guser.user_id()

            findRequest = BranchDetails.query()

            branchList = findRequest.fetch()
            strReqForEmployeeRegister = Guser.email()

            template = template_env.get_template('templates/employees.html')
            context = {'branches': branchList,'vstrReqForEmployeeRegister':strReqForEmployeeRegister,
                       'vstrReqReference': Guser.user_id()}
            self.response.write(template.render(context))
        else:
            template = template_env.get_template('templates/500.html')
            context = {}
            self.response.write(template.render(context))


class EmployeeLeadsHandler(webapp2.RequestHandler):
    def get(self):
        Guser = users.get_current_user()

        if Guser:

            findRequests = UserRights.query(UserRights.strReference == Guser.user_id())
            RightsList = findRequests.fetch()

            Rights = UserRights()

            if len(RightsList) > 0:
                Rights = RightsList[0]


            if users.is_current_user_admin() or ((Rights.bolAccessToEmployeesLeadsForm == True) and (Rights.bolEmployeesAdminFormReadAccess == True)):

                strAccessGranted = "YES"

                findRequests = Leads.query()
                LeadsList = findRequests.fetch()

                template = template_env.get_template('templates/leads.html')
                context = {'LeadsList':LeadsList}
                self.response.write(template.render(context))
            else:
                strAccessGranted = "NO"
                template = template_env.get_template('templates/500.html')
                context = {'vstrResourceName': "Leads Form"}
                self.response.write(template.render(context))

        else:
            template = template_env.get_template('templates/500.html')
            context = {'vstrResourceName': "Leads Form"}
            self.response.write(template.render(context))


class EmployeeFuneralCoversHandler(webapp2.RequestHandler):

    def get(self):

        Guser = users.get_current_user()
        logging.info("Employee Funeral Called")
        if Guser:

            findRequests = UserRights.query(UserRights.strReference == Guser.user_id())
            RightsList = findRequests.fetch()

            Rights = UserRights()

            if len(RightsList) > 0:
                Rights = RightsList[0]
            else:
                pass

            if users.is_current_user_admin() or ((Rights.bolAccessToEmployeesFuneralForm == True) and (Rights.bolEmployeesFuneralCoverFormReadAccess == True )):

                findRequest = WorkingPolicy.query(WorkingPolicy.strReference == Guser.user_id(), WorkingPolicy.strActivated == False)
                WorkingPolicyList = findRequest.fetch()

                WorkPol = WorkingPolicy()

                if len(WorkingPolicyList) > 0:
                    WorkPol = WorkingPolicyList[0]
                    logging.info("Working Policy Found")
                else:
                    findRequest = WorkingPolicy.query()
                    WorkPolList = findRequest.fetch()
                    WorkPol.writePolicyNum(strinput=WorkPol.createNewPolicyNumber(strinput=(len(WorkPolList) + 1)))
                    logging.info("Working Policy not Found New One Created")

                findRequest = ClientsPersonalDetails.query(ClientsPersonalDetails.strPolicyNum == WorkPol.strPolicyNum)
                PersonalDetailsList = findRequest.fetch()
                PersonalDetails = ClientsPersonalDetails()

                if len(PersonalDetailsList) > 0:
                    PersonalDetails = PersonalDetailsList[0]
                else:
                    pass

                findRequest = ClientsResidentialAddress.query(ClientsResidentialAddress.strPolicyNum == WorkPol.strPolicyNum)
                ClientsResidentialList = findRequest.fetch()
                Residential = ClientsResidentialAddress()

                if len(ClientsResidentialList) > 0:
                    Residential = ClientsResidentialList[0]
                else:
                    pass

                findRequest = ClientsPostalAddress.query(ClientsPostalAddress.strPolicyNum == WorkPol.strPolicyNum)
                ClientPostalList = findRequest.fetch()

                Postal = ClientsPostalAddress()
                if len(ClientPostalList) > 0:
                    Postal = ClientPostalList[0]
                else:
                    pass

                findRequest = ClientsContactDetails.query(ClientsContactDetails.strPolicyNum == WorkPol.strPolicyNum)
                ClientContactList = findRequest.fetch()

                Contacts = ClientsContactDetails()
                if len(ClientContactList) > 0:
                    Contacts = ClientContactList[0]
                else:
                    pass

                findRequest = Policy.query(Policy.strActivatePolicy == True)
                PolicyList = findRequest.fetch()
                ActiveClientList = []
                for pol in PolicyList:
                    findRequest = ClientsPersonalDetails.query(ClientsPersonalDetails.strPolicyNum == pol.strPolicyNum)
                    ClientList = findRequest.fetch()
                    if len(ClientList) > 0:
                        ActiveClientList.append(ClientList[0])



                template = template_env.get_template('templates/EmployeeFuneral.html')



                if Rights.bolEmployeesFuneralCoverFormWriteAccess == True:

                    bolFuneralCoverEditAccess = "YES"
                    logging.info("ITS A BIG YES")
                else:
                    bolFuneralCoverEditAccess = "NO"
                    logging.info("ITS A BIG NO")

                context = {'bolFuneralCoverEditAccess':bolFuneralCoverEditAccess,'vstrPolicyNumber': WorkPol.strPolicyNum, 'vstrTitle': PersonalDetails.readTitle(),
                           'vstrSurname': PersonalDetails.readSurname(),
                           'vstrFullnames': PersonalDetails.readNames(),
                           'vstrIDNumber': PersonalDetails.readIDNumber(),
                           'vstrDateofBirth': PersonalDetails.readDateOfBirth(),
                           'vstrNationality': PersonalDetails.readNationality(),
                           'vstrResidential1': Residential.readResAddressL1(),
                           'vstrResidential2': Residential.readResAddressL2(),
                           'vstrResidentialProvince': Residential.readProvince(),
                           'vstrResidentialCountry': Residential.readCountry(),
                           'vstrResidentialPostalCode': Residential.readPostalCode(),
                           'vstrPostalAddress1': Postal.readPostalAddressL1(),
                           'vstrPostalAddressCityTown': Postal.readTownCity(),
                           'vstrPostalProvince': Postal.readProvince(), 'vstrPostalCountry': Postal.readCountry(),
                           'vstrPostalCode': Postal.readPostalCode(),
                           'vstrDayTimeNumber': Contacts.readTell(), 'vstrCellNumber': Contacts.readCell(),
                           'vstrEmail': Contacts.readEmail(),'PolicyList': ActiveClientList}
                self.response.write(template.render(context))
            else:
                template = template_env.get_template('templates/500.html')
                context = {}
                self.response.write(template.render(context))

        else:
            template = template_env.get_template('templates/500.html')
            context = {}
            self.response.write(template.render(context))

    def post(self):
        Guser = users.get_current_user()

        if Guser:
            logging.info(msg="Policy Holder Create Policy Handler Called")
            strPolicyNumber = self.request.get('vstrPolicyNumber')
            strTitle = self.request.get('vstrTitle')
            strSurname = self.request.get('vstrSurname')
            strFullnames = self.request.get('vstrFullnames')
            strIDNumber = self.request.get('vstrIDNumber')
            strDateOfBirth = self.request.get('vstrDateofBirth')
            strNationality = self.request.get('vstrNationality')

            strResLine1 = self.request.get('vstrResidential1')
            strResLine2 = self.request.get('vstrResidential2')
            strResCountry = self.request.get('vstrResidentialCountry')
            strReProvince = self.request.get('vstrResidentialProvince')
            strResPostalCode = self.request.get('vstrResidentialPostalCode')

            strPosLine1 = self.request.get('vstrPostalAddress1')
            strPosCityTown = self.request.get('vstrPostalAddressCityTown')
            strPosCountry = self.request.get('vstrPostalCountry')
            strPosProvince = self.request.get('vstrPostalProvince')
            strPosPostalCode = self.request.get('vstrPostalCode')

            strDayTimeNumber = self.request.get('vstrDayTimeNumber')
            strCell = self.request.get('vstrCellNumber')
            strEmail = self.request.get('vstrEmail')



            ClientPersonal = ClientsPersonalDetails()

            findRequest = ClientsPersonalDetails.query(ClientsPersonalDetails.strPolicyNum == strPolicyNumber)
            ClientPersonalList = findRequest.fetch()

            if len(ClientPersonalList) > 0:
                ClientPersonal = ClientPersonalList[0]

            if not (strPolicyNumber == ""):
                ClientPersonal.writeReference(strinput=Guser.user_id())
                ClientPersonal.writePolicyNum(strinput=strPolicyNumber)
                ClientPersonal.writeNames(strinput=strFullnames)
                ClientPersonal.writeSurname(strinput=strSurname)
                ClientPersonal.writeIDNumber(strinput=strIDNumber)
                ClientPersonal.writeTitle(strinput=strTitle)
                ClientPersonal.writeDateOfBirth(strinput=strDateOfBirth)
                ClientPersonal.writeNationality(strinput=strNationality)

            Residential = ClientsResidentialAddress()

            findRequest = ClientsResidentialAddress.query(ClientsResidentialAddress.strPolicyNum == strPolicyNumber)
            ResidentialList = findRequest.fetch()

            if len(ResidentialList) > 0:
                Residential = ResidentialList[0]

            if not (strResLine1 == ""):
                Residential.writeReference(strinput=Guser.user_id())
                Residential.writePolicyNum(strinput=strPolicyNumber)
                Residential.writeResAddressL1(strinput=strResLine1)
                Residential.writeResAddressL2(strinput=strResLine2)
                Residential.writeProvince(strinput=strReProvince)
                Residential.writeCountry(strinput=strResCountry)
                Residential.writePostalCode(strinput=strResPostalCode)

            PostalAddy = ClientsPostalAddress()

            findRequest = ClientsPostalAddress.query(ClientsPostalAddress.strPolicyNum == strPolicyNumber)
            PostalAddyList = findRequest.fetch()

            if len(PostalAddyList) > 0:
                PostalAddy = PostalAddyList[0]

            if not (strPosLine1 == ""):
                PostalAddy.writeReference(strinput=Guser.user_id())
                PostalAddy.writePolicyNum(strinput=strPolicyNumber)
                PostalAddy.writePostalAddressL1(strinput=strPosLine1)
                PostalAddy.writeTownCity(strinput=strPosCityTown)
                PostalAddy.writeCountry(strinput=strPosCountry)
                PostalAddy.writeProvince(strinput=strPosProvince)
                PostalAddy.writePostalCode(strinput=strPosPostalCode)

            Contacts = ClientsContactDetails()

            findRequest = ClientsContactDetails.query(ClientsContactDetails.strPolicyNum == strPolicyNumber)
            ContactsList = findRequest.fetch()

            if len(ContactsList) > 0:
                Contacts = ContactsList[0]

            if not (strDayTimeNumber == ""):
                Contacts.writeReference(strinput=Guser.user_id())
                Contacts.writePolicyNum(strinput=strPolicyNumber)
                Contacts.writeCell(strinput=strCell)
                Contacts.writeTel(strinput=strDayTimeNumber)
                Contacts.writeEmail(strinput=strEmail)

            try:
                ClientPersonal.put()
                Residential.put()
                PostalAddy.put()
                Contacts.put()
            except:
                pass

            template = template_env.get_template('templates/dynamic/funeralpolicy/createpolicyholderresponse.html')
            context = {'vstrPolicyNumber' : strPolicyNumber , 'vstrFullnames' : strFullnames , 'vstrSurname' : strSurname,
                       'vstrIDNumber': strIDNumber, 'vstrCellNumber': strCell}

            self.response.write(template.render(context))


class EmployeeFuneralServiceHandler(webapp2.RequestHandler):
    def get(self):
        Guser = users.get_current_user()

        if Guser:
            findRequests = UserRights.query(UserRights.strReference == Guser.user_id())
            RightsList = findRequests.fetch()

            Rights = UserRights()

            if len(RightsList) > 0:
                Rights = RightsList[0]
            else:
                pass

            if users.is_current_user_admin() or ((Rights.bolAccessToEmployeesFuneralServiceForm == True) and (Rights.bolEmployeesFuneralCoverFormReadAccess == True)):

                template = template_env.get_template('templates/EmployeeFuneralService.html')
                context = {}
                self.response.write(template.render(context))
            else:
                template = template_env.get_template('templates/500.html')
                context = {}
                self.response.write(template.render(context))
        else:
            template = template_env.get_template('templates/500.html')
            context = {}
            self.response.write(template.render(context))


class EmployeeAdminHandler(webapp2.RequestHandler):
    def get(self):

        Guser = users.get_current_user()

        if Guser:
            findRequests = UserRights.query(UserRights.strReference == Guser.user_id())
            RightsList = findRequests.fetch()

            Rights = UserRights()

            if len(RightsList) > 0:
                Rights = RightsList[0]
            else:
                pass

            findRequests = BranchDetails.query()
            BranchList = findRequests.fetch()

            findRequest = PaymentHistory.query()
            TransactionList = findRequest.fetch()

            if users.is_current_user_admin or((Rights.bolEmployeesAdminFormReadAccess == True) and (Rights.bolAccessToEmployeesAdminForm == True)):
                template = template_env.get_template('templates/EmployeeAdmin.html')
                context = {'BranchList': BranchList,'TransactionList':TransactionList}
                self.response.write(template.render(context))
            else:
                template = template_env.get_template('templates/500.html')
                context = {'BranchList': BranchList}
                self.response.write(template.render(context))

        else:
            template = template_env.get_template('templates/500.html')
            context = {}
            self.response.write(template.render(context))



class ServicesFuneralCoverHandler(webapp2.RequestHandler):
    def get(self):
        Guser = users.get_current_user()

        if Guser:
            findRequests = UserRights.query(UserRights.strReference == Guser.user_id())
            RightsList = findRequests.fetch()

            Rights = UserRights()

            if len(RightsList) > 0:
                Rights = RightsList[0]
            else:
                pass

            if Rights.bolAccessToEmployeesFuneralServiceForm and Rights.bolEmployeesFuneralServicesFormReadAccess:
                template = template_env.get_template('templates/ServicesFuneralCover.html')
                context = {}
                self.response.write(template.render(context))
            else:
                template = template_env.get_template('templates/500.html')
                context = {}
                self.response.write(template.render(context))
        else:
            template = template_env.get_template('templates/500.html')
            context = {}
            self.response.write(template.render(context))


class ServicesFuneralServiceHandler(webapp2.RequestHandler):
    """
        Public Access
    """
    def get(self):


        template = template_env.get_template('templates/ServicesFuneralService.html')
        context = {}
        self.response.write(template.render(context))



class ClientsHandler(webapp2.RequestHandler):
    """
        Public Access
    """
    def get(self):
        template = template_env.get_template('templates/clients.html')
        context = {}
        self.response.write(template.render(context))

class ClientFuneralCoverHandler(webapp2.RequestHandler):
    def get(self):
        template = template_env.get_template('templates/ClientFuneral.html')
        context = {}
        self.response.write(template.render(context))


class ClientFuneralServiceHandler(webapp2.RequestHandler):
    def get(self):
        template = template_env.get_template('templates/ServicesFuneralService.html')
        context = {}
        self.response.write(template.render(context))

class ClientClaimsFormHandler(webapp2.RequestHandler):
    def get(self):
        template = template_env.get_template('templates/ClientClaimsForm.html')
        context = {}
        self.response.write(template.render(context))

class ClientReferralsHandler(webapp2.RequestHandler):
    def get(self):
        template = template_env.get_template('templates/ClientReferrals.html')
        context = {}
        self.response.write(template.render(context))

class ChatsHandler(webapp2.RequestHandler):
    def get(self):
        template = template_env.get_template('templates/chats.html')
        context = {}
        self.response.write(template.render(context))

class StaffChatHandler(webapp2.RequestHandler):
    def get(self):
        template = template_env.get_template('templates/StaffChat.html')
        context = {}
        self.response.write(template.render(context))

class UserChatHandler(webapp2.RequestHandler):
    def get(self):
        template = template_env.get_template('templates/UserChat.html')
        context = {}
        self.response.write(template.render(context))

class AboutHandler(webapp2.RequestHandler):
    def get(self):
        template = template_env.get_template('templates/about.html')
        context = {}
        self.response.write(template.render(context))

class ContactHandler(webapp2.RequestHandler):
    def get(self):
        template = template_env.get_template('templates/contact.html')
        context = {}
        self.response.write(template.render(context))




class AdminHandler(webapp2.RequestHandler):
    def get(self):
        template = template_env.get_template('templates/admin.html')
        context = {}
        self.response.write(template.render(context))

class TasksHandler(webapp2.RequestHandler):
    """
        Tasks handler must return only a sub HTML document with all the tasks and they must be rendered
         by the main document on display meaning this URL will be called dynamically by the active page
    """
    def get(self):
        template = template_env.get_template('templates/tasks.html')
        context = {}
        self.response.write(template.render(context))

class NotificationsHandler(webapp2.RequestHandler):
    def get(self):
        template = template_env.get_template('templates/notifications.html')
        context = {}
        self.response.write(template.render(context))

class InboxHandler(webapp2.RequestHandler):
    def get(self):
        template = template_env.get_template('templates/inbox.html')
        context = {}
        self.response.write(template.render(context))

app = webapp2.WSGIApplication([
    ('/services', ServicesHandler),
    ('/services/funeral-cover', ServicesFuneralCoverHandler),
    ('/services/funeral-services', ServicesFuneralServiceHandler),
    ('/employees', EmployeesHandler),
    ('/employees/leads', EmployeeLeadsHandler),

    ('/employees/funeral-cover', EmployeeFuneralCoversHandler),
    ('/employees/funeral-service', EmployeeFuneralServiceHandler),
    ('/employees/admin', EmployeeAdminHandler),

    ('/clients', ClientsHandler),
    ('/clients/funeral-cover', ClientFuneralCoverHandler),
    ('/clients/funeral-service', ClientFuneralServiceHandler),
    ('/clients/claims', ClientClaimsFormHandler),
    ('/clients/referrals', ClientReferralsHandler),

    ('/chats',ChatsHandler),
    ('/chats/staff', StaffChatHandler),
    ('/chats/users', UserChatHandler),

    ('/about', AboutHandler),
    ('/contact', ContactHandler),

    ('/tasks', TasksHandler),
    ('/notifications',NotificationsHandler),
    ('/inbox', InboxHandler),

    ('/admin', AdminHandler),
    ('/', MainHandler)
], debug=True)


