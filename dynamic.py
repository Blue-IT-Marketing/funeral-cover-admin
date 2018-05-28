






import os
import webapp2
import jinja2
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import ndb
from google.appengine.api import users
import logging
template_env = jinja2.Environment(
loader=jinja2.FileSystemLoader(os.getcwd()))
from database import ClientsPersonalDetails,ClientsResidentialAddress,ClientsPostalAddress,ClientsContactDetails, ChildrenDetails, WorkingPolicy

from Employee import EmployeeConst,BranchDetails,EmploymentDetails, PostalAddress, ResidentialAddress,BankingDetails,ContactDetails

from database import Spouses, ChildrenDetails, ExtendedFamily,ClientsPersonalDetails,Beneficiary,UserRights

class SpouseDynamicHandler(webapp2.RequestHandler):
    def get(self):
        Guser = users.get_current_user()

        if Guser:

            strPolicyNumber = self.request.get('vstrPolicyNumber')



            findRequest = Spouses.query(Spouses.strPolicyNum == strPolicyNumber)
            SpousesList = findRequest.fetch()

            template = template_env.get_template('templates/dynamic/funeralpolicy/Spouse.html')
            context = {'SpouseList' : SpousesList}
            self.response.write(template.render(context))


    def post(self):
        Guser = users.get_current_user()

        if Guser:

            strPolicyNumber = self.request.get('vstrPolicyNumber')
            strFullNames = self.request.get('vstrFullNames')
            strSurname = self.request.get('vstrSurname')
            strIDNumber = self.request.get('vstrIDNumber')
            strDateOfBirth = self.request.get('vstrDateOfBirth')
            logging.info(strIDNumber)
            strRelationship = self.request.get('vstrRelationship')

            SpouseInfo = Spouses()

            findRequest = Spouses.query(Spouses.strIDNumber == strIDNumber)
            SpouseList = findRequest.fetch()

            Error = False

            if len(SpouseList) > 0:
                template = template_env.get_template('templates/dynamic/funeralpolicy/Spouse.html')
                context = {'MessageDiag': "Error Already Added as Spouse on Another Policy"}
                self.response.write(template.render(context))
                Error = True
            else:
                pass

            findRequest = ChildrenDetails.query(ChildrenDetails.strIDNumber == strIDNumber)
            ChildList = findRequest.fetch()

            if len(ChildList) > 0:
                template = template_env.get_template('templates/dynamic/funeralpolicy/Spouse.html')
                context = {'MessageDiag': "Error Already Added as Child on Another Policy"}
                self.response.write(template.render(context))
                Error = True
            else:
                pass


            findRequest = ExtendedFamily.query(ExtendedFamily.strIDNumber == strIDNumber)
            ExtendedList = findRequest.fetch()

            if len(ExtendedList) > 0:
                template = template_env.get_template('templates/dynamic/funeralpolicy/Spouse.html')
                context = {'MessageDiag': "Error Already Added as Child on Another Policy"}
                self.response.write(template.render(context))
                Error = True
            else:
                pass

            findRequest = ClientsPersonalDetails.query(ClientsPersonalDetails.strIDNumber == strIDNumber)
            PrincipalList = findRequest.fetch()

            if len(PrincipalList) > 0:
                template = template_env.get_template('templates/dynamic/funeralpolicy/Spouse.html')
                context = {'MessageDiag': "Error Already Added as Child on Another Policy"}
                self.response.write(template.render(context))
                Error = True
            else:
                pass


            if not(Error):
                SpouseInfo.writePolicyNum(strinput=strPolicyNumber)
                SpouseInfo.writeReference(strinput=Guser.user_id())
                SpouseInfo.writeIDNumber(strinput=strIDNumber)
                SpouseInfo.writeNames(strinput=strFullNames)
                SpouseInfo.writeSurname(strinput=strSurname)
                SpouseInfo.writeRelationship(strinput=strRelationship)
                SpouseInfo.writeDateOfBirth(strinput=strDateOfBirth)

                SpouseInfo.put()

                findRequest = Spouses.query(Spouses.strPolicyNum == strPolicyNumber)
                SpouseList = findRequest.fetch()


                template = template_env.get_template('templates/dynamic/funeralpolicy/Spouse.html')
                context = {'MessageDiag': "Spouse Succesfully Added", 'SpouseList': SpouseList}
                self.response.write(template.render(context))
            else:
                pass



class ChildrenDynamicHandler(webapp2.RequestHandler):
    def get(self):
        Guser = users.get_current_user()

        if Guser:

            strPolicyNumber = self.request.get('vstrPolicyNumber')

            findRequest = ChildrenDetails.query(ChildrenDetails.strPolicyNum == strPolicyNumber)
            ChildrenList = findRequest.fetch()



            template = template_env.get_template('templates/dynamic/funeralpolicy/Children.html')
            context = {'ChildrenList': ChildrenList}
            self.response.write(template.render(context))
        else:
            pass


    def post(self):
        Guser = users.get_current_user()

        if Guser:
            strPolicyNumber = self.request.get('vstrPolicyNumber')
            strFullNames = self.request.get('vstrFullNames')
            strSurname = self.request.get('vstrSurname')
            strIDNumber = self.request.get('vstrIDNumber')

            strDateofBirth = self.request.get('vstrDateofBirth')
            logging.info(strDateofBirth)
            strRelationship = self.request.get('vstrRelationship')

            strIDNumber = str(strIDNumber)
            strIDNumber = strIDNumber.strip()

            findRequest = Spouses.query(Spouses.strIDNumber == strIDNumber)
            SpouseList = findRequest.fetch()

            Error = False

            if len(SpouseList) > 0:
                template = template_env.get_template('templates/dynamic/funeralpolicy/Children.html')
                context = {'MessageDiag': "Error Already Added as Spouse on Another Policy"}
                self.response.write(template.render(context))
                Error = True
            else:
                pass

            findRequest = ChildrenDetails.query(ChildrenDetails.strIDNumber == strIDNumber)
            ChildrenList = findRequest.fetch()

            if len(ChildrenList) > 0:
                template = template_env.get_template('templates/dynamic/funeralpolicy/Children.html')
                context = {'MessageDiag': "Error Already Added as Child on Another Policy"}
                self.response.write(template.render(context))
                Error = True
            else:
                pass


            findRequest = ExtendedFamily.query(ExtendedFamily.strIDNumber == strIDNumber)
            ExtendedList = findRequest.fetch()

            if len(ExtendedList) > 0:
                template = template_env.get_template('templates/dynamic/funeralpolicy/Children.html')
                context = {'MessageDiag': "Error Already Added as an Extended Member on Another Policy"}
                self.response.write(template.render(context))
                Error = True
            else:
                pass

            findRequest = ClientsPersonalDetails.query(ClientsPersonalDetails.strIDNumber == strIDNumber)
            PrincipalList = findRequest.fetch()

            if len(PrincipalList) > 0:
                template = template_env.get_template('templates/dynamic/funeralpolicy/Children.html')
                context = {'MessageDiag': "Error Already Added as Principal Member on Another Policy"}
                self.response.write(template.render(context))
                Error = True
            else:
                pass


            if not(Error):
                Child = ChildrenDetails()
                Child.writeReference(strinput=Guser.user_id())
                Child.writePolicyNum(strinput=strPolicyNumber)
                Child.writeIDNumber(strinput=strIDNumber)
                Child.writeDateOfBirth(strinput=strDateofBirth)
                Child.writeNames(strinput=strFullNames)
                Child.writeSurname(strinput=strSurname)
                Child.writeRelationship(strinput=strRelationship)
                Child.put()

                findRequest = ChildrenDetails.query(ChildrenDetails.strPolicyNum == strPolicyNumber)
                ChildList = findRequest.fetch()


                template = template_env.get_template('templates/dynamic/funeralpolicy/Children.html')
                context = {'ChildrenList': ChildList}
                self.response.write(template.render(context))


class ExtendedDynamicHandler(webapp2.RequestHandler):
    def get(self):
        Guser = users.get_current_user()
        if Guser:
            strPolicyNumber = self.request.get('vstrPolicyNumber')

            findRequest = ExtendedFamily.query(ExtendedFamily.strPolicyNum == strPolicyNumber)
            ExtendedList = findRequest.fetch()

            template = template_env.get_template('templates/dynamic/funeralpolicy/Extended.html')
            context = {'ExtendedFamilyList':ExtendedList}
            self.response.write(template.render(context))

        else:
            pass

    def post(self):
        Guser = users.get_current_user()

        if Guser:
            strPolicyNumber = self.request.get('vstrPolicyNumber')
            strFullNames = self.request.get('vstrFullNames')
            strSurname = self.request.get('vstrSurname')
            strIDNumber = self.request.get('vstrIDNumber')

            strDateofBirth = self.request.get('vstrDateofBirth')
            logging.info(strDateofBirth)
            strRelationship = self.request.get('vstrRelationship')

            strIDNumber = str(strIDNumber)
            strIDNumber = strIDNumber.strip()

            findRequest = ExtendedFamily.query(ExtendedFamily.strIDNumber == strIDNumber)
            ExtendedList = findRequest.fetch()

            Error = False

            if len(ExtendedList) > 0:
                template = template_env.get_template('templates/dynamic/funeralpolicy/Extended.html')
                context = {'MessageDiag': "Error Already Added as Extended on Another Policy"}
                self.response.write(template.render(context))
                Error = True
            else:
                pass


            findRequest = Spouses.query(Spouses.strIDNumber == strIDNumber)
            SpouseList = findRequest.fetch()

            if len(SpouseList) > 0:
                template = template_env.get_template('templates/dynamic/funeralpolicy/Extended.html')
                context = {'MessageDiag': "Error Already Added as Spouse on Another Policy"}
                self.response.write(template.render(context))
                Error = True
            else:
                pass

            findRequest = ChildrenDetails.query(ChildrenDetails.strIDNumber == strIDNumber)
            ChildList = findRequest.fetch()

            if len(ChildList) > 0:
                template = template_env.get_template('templates/dynamic/funeralpolicy/Extended.html')
                context = {'MessageDiag': "Error Already Added as Child on Another Policy"}
                self.response.write(template.render(context))
                Error = True
            else:
                pass


            findRequest = ClientsPersonalDetails.query(ClientsPersonalDetails.strIDNumber == strIDNumber)
            PolicyHolderList = findRequest.fetch()

            if len(PolicyHolderList) > 0:
                template = template_env.get_template('templates/dynamic/funeralpolicy/Extended.html')
                context = {'MessageDiag': "Error Already Added as Child on Another Policy"}
                self.response.write(template.render(context))
                Error = True
            else:
                pass


            if not(Error):
                Extended = ExtendedFamily()

                Extended.writeReference(strinput=Guser.user_id())
                Extended.writePolicyNum(strinput=strPolicyNumber)
                Extended.writeNames(strinput=strFullNames)
                Extended.writeSurname(strinput=strSurname)
                Extended.writeIDNumber(strinput=strIDNumber)
                Extended.writeRelationship(strinput=strRelationship)
                Extended.writeDateOfBirth(strinput=strDateofBirth)
                Extended.put()

                findRequest = ExtendedFamily.query(ExtendedFamily.strPolicyNum == strPolicyNumber)
                ExtendedList = findRequest.fetch()

                template = template_env.get_template('templates/dynamic/funeralpolicy/Extended.html')
                context = {'ExtendedFamilyList': ExtendedList}
                self.response.write(template.render(context))

            else:
                pass


class BeneficiaryDynamicHandler(webapp2.RequestHandler):
    def get(self):
        Guser = users.get_current_user()

        if Guser:

            strPolicyNumber = self.request.get('vstrPolicyNumber')

            findRequest = Beneficiary.query(Beneficiary.strPolicyNum == strPolicyNumber)
            BeneficiaryList = findRequest.fetch()




            template = template_env.get_template('templates/dynamic/funeralpolicy/Beneficiary.html')
            context = {'BeneficiaryList': BeneficiaryList}
            self.response.write(template.render(context))


    def post(self):
        Guser = users.get_current_user()

        if Guser:
            strPolicyNumber = self.request.get('vstrPolicyNumber')
            strFullNames = self.request.get('vstrFullNames')
            strSurname = self.request.get('vstrSurname')
            strIDNumber = self.request.get('vstrIDNumber')
            strDateofBirth = self.request.get('vstrDateofBirth')
            strRelationship = self.request.get('vstrRelationship')

            Beneficy = Beneficiary()

            Beneficy.writePolicyNum(strinput=strPolicyNumber)
            Beneficy.writeReference(strinput=Guser.user_id())
            Beneficy.writeNames(strinput=strFullNames)
            Beneficy.writeSurname(strinput=strSurname)
            Beneficy.writeIDNumber(strinput=strIDNumber)
            Beneficy.writeDateOfBirth(strinput=strDateofBirth)
            Beneficy.writeRelationship(strinput=strRelationship)

            Beneficy.put()

            findRequest = Beneficiary.query(Beneficiary.strPolicyNum == strPolicyNumber)
            BeneficiaryList = findRequest.fetch()


            template = template_env.get_template('templates/dynamic/funeralpolicy/Beneficiary.html')
            context = {'BeneficiaryList': BeneficiaryList}
            self.response.write(template.render(context))


class SingleDynamicHandler(webapp2.RequestHandler):
    def get(self):
        template = template_env.get_template('templates/dynamic/funeralpolicy/Single.html')
        context = {}
        self.response.write(template.render(context))

class FamilyDynamicHandler(webapp2.RequestHandler):
    def get(self):
        template = template_env.get_template('templates/dynamic/funeralpolicy/Family.html')
        context = {}
        self.response.write(template.render(context))

class ExtendedCoverDynamicHandler(webapp2.RequestHandler):
    def get(self):
        template = template_env.get_template('templates/dynamic/funeralpolicy/ExtendedCover.html')
        context = {}
        self.response.write(template.render(context))

class SeniorMemberCoverDynamicHandler(webapp2.RequestHandler):
    def get(self):
        template = template_env.get_template('templates/dynamic/funeralpolicy/SeniorMemberBenefits.html')
        context = {}
        self.response.write(template.render(context))
class AmountPayableDynamicHandler(webapp2.RequestHandler):
    def get(self):
        template = template_env.get_template('templates/dynamic/funeralpolicy/AmountPayableSummary.html')
        context = {}
        self.response.write(template.render(context))
class PaymentDetailsDynamicHandler(webapp2.RequestHandler):
    def get(self):
        upload_url = blobstore.create_upload_url('/funeral/paymentdetails/payroll')
        logging.info(upload_url)
        template = template_env.get_template('templates/dynamic/funeralpolicy/PaymentDetails.html')
        context = {'payroll_upload': upload_url}
        self.response.write(template.render(context))





class EditBranchHandler(webapp2.RequestHandler):
    def get(self):
        logging.info(msg="Edit Branch Handler Was Called")
        Guser = users.get_current_user()
        if Guser:
            findQuery = BranchDetails.query()
            results = findQuery.fetch()

            if len(results) > 0:
                branchdet = results
            else:
                branchdet = []

            template = template_env.get_template('templates/dynamic/admin/editbranch.html')
            context = {'branches': branchdet }
            self.response.write(template.render(context))
        else:
            pass

    def post(self):
        logging.info(msg="Branch Saving Data")
        Guser = users.get_current_user()
        if Guser:
            strBranchName = self.request.get('vstrBranchName')
            strBranchCode = self.request.get('vstrBranchCode')
            strBranchAddress = self.request.get('vstrBranchAddress')
            strBranchContact = self.request.get('vstrBranchContact')
            strBranchEmail = self.request.get('vstrBranchEmail')
            strBranchManager = self.request.get('vstrBranchManager')
            strBranchManagerContact = self.request.get('vstrBranchManagerContact')
            strBranchManagerEmail = self.request.get('vstrBranchManagerEmail')

            newBranch = BranchDetails()

            findRequest = BranchDetails.query(BranchDetails.strCompanyBranchCode == strBranchCode)
            TempBranchList = findRequest.fetch()

            if len(TempBranchList) > 0:
                newBranch = TempBranchList[0]

            if newBranch.writeCompanyBranchName(strBranchName) and newBranch.writeCompanyBranchCode(strBranchCode):
                newBranch.writeReference(strinput=Guser.user_id())
                newBranch.writeCompanyBranchTel(strinput=strBranchContact)
                newBranch.writeCompanyBranchAddress(strinput=strBranchAddress)
                newBranch.writeCompanyBranchEmail(strinput=strBranchEmail)
                newBranch.writeBranchManagerName(strinput=strBranchManager)
                newBranch.writeBranchManagerTel(strinput=strBranchManagerContact)
                newBranch.writeBranchManagerEmail(strinput=strBranchManagerEmail)
                newBranch.put()
                self.redirect("/admin")
            else:
                self.redirect("/admin")
        else:
            self.redirect("/admin")


class EditEmployeesHandler(webapp2.RequestHandler):

    def get(self):
        logging.info(msg="Edit Branch Handler was called")
        Guser = users.get_current_user()

        if Guser:
            findQuery = EmploymentDetails.query()
            results = findQuery.fetch()

            if len(results) > 0:
                employeesdet = results
            else:
                employeesdet = []

            findQuery = BranchDetails.query()
            results = findQuery.fetch()

            if len(results) > 0:
                branchdet = results
            else:
                branchdet = []

            template = template_env.get_template('templates/dynamic/admin/editemployees.html')
            context = {'employees': employeesdet,
                       'branches': branchdet}
            self.response.write(template.render(context))
        else:
            pass

    def post(self):
        Guser = users.get_current_user()

        if Guser:
            strBranchCode = self.request.get('vstrBranchCode')
            strEmployeeCode = self.request.get('vstrEmployeeCode')
            strContractType = self.request.get('vstrContractType')
            strBasicSalary = self.request.get('vstrBasicSalary')
            strDateOfEmployment = self.request.get('vstrDateOfEmployment')
            strTitle = self.request.get('vstrTitle')
            strFullnames = self.request.get('vstrFullnames')
            strSurname = self.request.get('vstrSurname')
            strIDNumber = self.request.get('vstrIDNumber')
            strDateOfBirth = self.request.get('vstrDateOfBirth')
            strNationality = self.request.get('vstrNationality')
            strPhysicalAddressL1 = self.request.get('vstrPhysicalAddressL1')
            strPhysicalAddressL2 = self.request.get('vstrPhysicalAddressL2')
            strCityTown = self.request.get('vstrCityTown')
            strProvince  = self.request.get('vstrProvince')
            strPhysicalPostalCode = self.request.get('vstrPhysicalPostalCode')
            strPostalAddressL1 = self.request.get('vstrPostalAddressL1')
            strPostalAddressL2 = self.request.get('vstrPostalAddressL2')
            strPostalCityTown = self.request.get('vstrPostalCityTown')
            strPostalProvince = self.request.get('vstrPostalProvince')
            strPostalCode = self.request.get('vstrPostalCode')

            strAccountHolder = self.request.get('vstrAccountHolder')
            strBankName = self.request.get('vstrBankName')
            strAccountType = self.request.get('vstrAccountType')
            strAccountNumber = self.request.get('vstrAccountNumber')
            strBankBranchCode = self.request.get('vstrBankBranchCode')

            strCell = self.request.get('vstrCell')
            strTel = self.request.get('vstrTel')
            strEmail = self.request.get('vstrEmail')

            findRequest = EmploymentDetails.query(EmploymentDetails.strEmployeeCode == strEmployeeCode)
            EmpResult = findRequest.fetch()

            if len(EmpResult) > 0:
                Employee = EmpResult[0]
            else:
                Employee = EmploymentDetails()


            try:
                Employee.writeEmployeeCode(strinput=strEmployeeCode)
                Employee.writeBranchWorking(strinput=strBranchCode)
                Employee.writeContractType(strinput=strContractType)
                Employee.writeBasicSalary(strinput=strBasicSalary)
                Employee.writeDateOfEmployment(strinput=strDateOfEmployment)
                Employee.writeTitle(strinput=strTitle)
                Employee.writeNames(strinput=strFullnames)
                Employee.writeSurname(strinput=strSurname)
                Employee.writeIDNumber(strinput=strIDNumber)
                Employee.writeDateOfBirth(strinput=strDateOfBirth)
                Employee.writeNationality(strinput=strNationality)

                Employee.put()
            except:
                pass

            findRequest = ResidentialAddress.query(ResidentialAddress.strEmployeeCode == strEmployeeCode)
            PhysicalResult = findRequest.fetch()


            if len(PhysicalResult) > 0:
                PhysicalAddress = PhysicalResult[0]
            else:
                PhysicalAddress = ResidentialAddress()

            try:
                PhysicalAddress.writeEmployeeCode(strinput=strEmployeeCode)
                PhysicalAddress.writeResAddressL1(strinput=strPhysicalAddressL1)
                PhysicalAddress.writeResAddressL2(strinput=strPhysicalAddressL2)
                PhysicalAddress.writeCityTown(strinput=strCityTown)
                PhysicalAddress.writeProvince(strinput=strProvince)
                PhysicalAddress.writePostalCode(strinput=strPhysicalPostalCode)

                PhysicalAddress.put()
            except:
                pass

            findRequest = PostalAddress.query(PostalAddress.strEmployeeCode == strEmployeeCode)
            PostalList = findRequest.fetch()


            if len(PostalList) > 0:
                PostalAddy = PostalList[0]
            else:
                PostalAddy = PostalAddress()

            try:
                PostalAddy.writeEmployeeCode(strinput=strEmployeeCode)
                PostalAddy.writePostalAddressL1(strinput=strPostalAddressL1)
                PostalAddy.writePostalAddressL2(strinput=strPostalAddressL2)
                PostalAddy.writeTownCity(strinput=strPostalCityTown)
                PostalAddy.writeProvince(strinput=strPostalProvince)
                PostalAddy.writePostalCode(strinput=strPostalCode)

                PostalAddy.put()
            except:
                pass

            findRequest = ContactDetails.query(ContactDetails.strEmployeeCode == strEmployeeCode)
            ContactList = findRequest.fetch()

            if len(ContactList) > 0:
                Contacts = ContactList[0]
            else:
                Contacts = ContactDetails()
            try:
                Contacts.writeEmployeeCode(strinput=strEmployeeCode)
                Contacts.writeCell(strinput=strCell)
                Contacts.writeTel(strinput=strTel)
                Contacts.writeEmail(strinput=strEmail)


                Contacts.put()
            except:
                pass


            findRequester = BankingDetails.query(BankingDetails.strEmployeeCode == strEmployeeCode)
            BankingList = findRequester.fetch()

            if len(BankingList) > 0:
                Banking = BankingList[0]
            else:
                Banking = BankingDetails()


            try:
                Banking.writeEmployeeCode(strinput=strEmployeeCode)
                Banking.writeAccountHolder(strinput=strAccountHolder)
                Banking.writeAccountNumber(strinput=strAccountNumber)
                Banking.writeAccountType(strinput=strAccountType)
                Banking.writeBankName(strinput=strBankName)
                Banking.writeBranchCode(strinput=strBankBranchCode)

                Banking.put()
            except:
                pass

            findRequest = WorkingPolicy.query(WorkingPolicy.strReference == Employee.strReference)
            AllOpenPolicies = findRequest.fetch()
            try:
                for OpenPols in AllOpenPolicies:
                    OpenPols.strActivated = True
                    OpenPols.put()
            except:
                pass

            findRequest = UserRights.query(UserRights.strReference == Employee.strReference)
            UserRightsList = findRequest.fetch()

            if len(UserRightsList) > 0:
                EmployeeRights = UserRightsList[0]
                EmployeeRights.writeEmployeeCode(strinput=strEmployeeCode)
                EmployeeRights.put()


            self.redirect('/admin')
        else:
            self.redirect('/admin')





app = webapp2.WSGIApplication([

    ('/dynamic/funeralpolicy/Spouse.html', SpouseDynamicHandler),
    ('/dynamic/funeralpolicy/Children.html', ChildrenDynamicHandler),
    ('/dynamic/funeralpolicy/Extended.html', ExtendedDynamicHandler),
    ('/dynamic/funeralpolicy/Beneficiary.html', BeneficiaryDynamicHandler),
    ('/dynamic/funeralpolicy/Single.html', SingleDynamicHandler),
    ('/dynamic/funeralpolicy/Family.html', FamilyDynamicHandler),
    ('/dynamic/funeralpolicy/ExtendedCover.html', ExtendedCoverDynamicHandler),
    ('/dynamic/funeralpolicy/SeniorMemberBenefits.html', SeniorMemberCoverDynamicHandler),
    ('/dynamic/funeralpolicy/AmountPayableSummary.html', AmountPayableDynamicHandler),
    ('/dynamic/funeralpolicy/PaymentDetails.html', PaymentDetailsDynamicHandler),
    ('/dynamic/admin/editbranch.html', EditBranchHandler),
    ('/dynamic/admin/editemployees.html', EditEmployeesHandler)


], debug=True)
