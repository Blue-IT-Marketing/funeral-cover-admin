import os
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
import webapp2
import jinja2
from google.appengine.ext import ndb
from google.appengine.api import users
import logging
template_env = jinja2.Environment(
loader=jinja2.FileSystemLoader(os.getcwd()))

import datetime

from database import ChildrenDetails,Spouses, ExtendedFamily, Beneficiary,Policy,WorkingPolicy,ClientsPersonalDetails,ClientsResidentialAddress
from database import ClientsPersonalDetails, ClientsContactDetails,PaymentHistory,ClientsPostalAddress,Claims
from PaymentsDetails import DirectDeposit,DebitOrder,Cash
from covers import Covers,num_years


class SMS(ndb.Expando):
    strToCellNumber = ndb.StringProperty()
    strMessage = ndb.StringProperty()

    def sendSMS(self,strCell,strMessage):
        pass
class Emails(ndb.Expando):
    strToEmail = ndb.StringProperty()
    strSubject = ndb.StringProperty()
    strMessage = ndb.StringProperty()
    strToName = ndb.StringProperty()

    def sendEmailNotification(self,strEmail,strSubject,strMessage):
        pass

class FuneralCoverCreateFamilyHandler(webapp2.RequestHandler):
    def get(self):
        Guser = users.get_current_user()

        try:

            if Guser:
                strPolicyNum = self.request.get('vstrPolicyNumber')
                strPolicyNum = str(strPolicyNum)
                logging.info("Policy Number on Create Family Handler : " + strPolicyNum)


                strFamilyPlanChoice = self.request.get('vstrFamilyPlanChoice')
                strFamilyPlanChoice = str(strFamilyPlanChoice)
                strFamilyPlanChoice = strFamilyPlanChoice.strip()
                strPaymentDay = self.request.get('vstrPaymentDay')
                strPaymentDay = str(strPaymentDay).strip()
                strClientSignature = self.request.get('vstrClientSignature')
                strClientSignature = strClientSignature.strip()
                strEmployeeSignature = self.request.get('vstrEmployeeSignature')
                strEmployeeSignature = strEmployeeSignature.strip()

                today = datetime.datetime.today()
                today = today.date()

                thisMonth = today.month
                thisYear = today.year

                if (thisMonth == 12):
                    thisMonth = 1
                    thisYear = today.year + 1
                else:
                    thisMonth = thisMonth + 1

                thisDay = int(strPaymentDay)

                strFirstPremiumDate = datetime.date(year=thisYear,month=thisMonth,day=thisDay)

                strPremium = 0
                if (strFamilyPlanChoice == "A"):
                    strPremium = 50
                elif (strFamilyPlanChoice == "B"):
                    strPremium = 60
                elif (strFamilyPlanChoice == "C"):
                    strPremium = 85
                elif (strFamilyPlanChoice == "D"):
                    strPremium = 95


                thisPolicy = Policy()
                findRequest = Covers.query(Covers.strCoverType == "Family")
                thisCover = findRequest.fetch()

                if len(thisCover) > 0:
                    thisCover = thisCover[0]
                else:
                    thisCover = Covers()

                findRequest = Policy.query(Policy.strPolicyNum == strPolicyNum)
                thisPolicyList = findRequest.fetch()

                if len(thisPolicyList) > 0:
                    thisPolicy = thisPolicyList[0]


                try:
                    thisPolicy.writeCoverCode(strinput=thisCover.readCoverCode())

                    thisPolicy.writeFirstPremiumDate(strinput=strFirstPremiumDate)

                    thisPolicy.writePaymentCode(strinput=strPolicyNum) # Payment Transactions Code
                    thisPolicy.writeReference(strinput=Guser.user_id())

                    thisPolicy.writePolicyNum(strinput=strPolicyNum)
                    thisPolicy.writePlanChoice(strinput=strFamilyPlanChoice)
                    thisPolicy.writeTotalPremiums(strinput=strPremium)

                    thisPolicy.writePaymentDay(strinput=strPaymentDay)
                    thisPolicy.writeClientSignature(strinput=strClientSignature)

                    thisPolicy.writeEmployeeSignature(strinput=strEmployeeSignature)

                    thisPolicy.put()
                except:
                    self.response.write("""<strong>ERROR :</strong>""")

                self.response.write("""
                <strong>Policy Created and Saved---Please Add Payment Details if you have not done so yet and then activate the Policy</h3>

                """)
            else:
                self.response.write("""
                 <strong>Policy not Saved</strong>
                 """)
        except:
            self.response.write("""

            <strong>Error Saving Policy</strong>

            """)

class FuneralCoverCreateSingleHandler(webapp2.RequestHandler):

    def get(self):
        Guser = users.get_current_user()

        if Guser:
            strPolicyNum = self.request.get('vstrPolicyNumber')
            strPolicyNum = str(strPolicyNum)
            strPolicyNum = strPolicyNum.strip()
            strSinglePlanChoice = self.request.get('vstrSinglePlanChoice')
            strSinglePlanChoice = str(strSinglePlanChoice)
            strSinglePlanChoice = strSinglePlanChoice.strip()
            strPaymentDay = self.request.get('vstrPaymentDay')
            strPaymentDay = str(strPaymentDay).strip()

            strClientSignature = self.request.get('vstrClientSignature')
            strClientSignature = strClientSignature.strip()
            strEmployeeSignature = self.request.get('vstrEmployeeSignature')
            strEmployeeSignature = strEmployeeSignature.strip()

            strPremiumCalculated = self.request.get('vstrTotalPremium')


            today = datetime.datetime.today()
            today = today.date()

            thisMonth = today.month
            thisYear = today.year

            if thisMonth == 12 :
                thisMonth = 1
                thisYear = today.year + 1
            else:
                thisMonth = thisMonth + 1

            thisDay = int(strPaymentDay)

            strFirstPremiumDate = datetime.date(year=thisYear,month=thisMonth,day=thisDay)



            thisPolicy = Policy()
            findRequest = Covers.query(Covers.strCoverType == "Single")
            thisCover = findRequest.fetch()

            if len(thisCover) > 0:
                thisCover = thisCover[0]
            else:
                thisCover = Covers()


            findRequest = Policy.query(Policy.strPolicyNum == strPolicyNum)
            thisPolicyList = findRequest.fetch()

            if len(thisPolicyList) > 0:
                thisPolicy = thisPolicyList[0]

            thisPolicy.writeCoverCode(strinput=thisCover.readCoverCode())
            thisPolicy.writeFirstPremiumDate(strinput=strFirstPremiumDate)
            thisPolicy.writePaymentCode(strinput=strPolicyNum) # Payment Transactions Code
            thisPolicy.writeReference(strinput=Guser.user_id())
            thisPolicy.writePolicyNum(strinput=strPolicyNum)
            thisPolicy.writeSinglePlanChoice(strinput=strSinglePlanChoice)
            thisPolicy.writeTotalPremiums(strinput=strPremiumCalculated)
            thisPolicy.writePaymentDay(strinput=strPaymentDay)
            thisPolicy.writeClientSignature(strinput=strClientSignature)
            thisPolicy.writeEmployeeSignature(strinput=strEmployeeSignature)
            thisPolicy.put()

            self.response.write("Policy Created and Saved---Please Add Payment Details if you have not done so yet and then activate the Policy")
        else:
            self.response.write("Policy not Saved")


class FuneralCoverCreateExtendedHandler(webapp2.RequestHandler):
    def get(self):

        Guser = users.get_current_user()

        if Guser:
            strPolicyNum = self.request.get('vstrPolicyNumber')
            strPolicyNum = str(strPolicyNum)
            strPolicyNum = strPolicyNum.strip()
            strFamilyPlanChoice = self.request.get('vstrFamilyPlanChoice')
            strFamilyPlanChoice = str(strFamilyPlanChoice)
            strFamilyPlanChoice = strFamilyPlanChoice.strip()
            strExtendedPlanChoice = self.request.get('vstrExtendedPlanChoice')
            strExtendedPlanChoice = strExtendedPlanChoice.strip()

            strPaymentDay = self.request.get('vstrPaymentDay')
            strPaymentDay = str(strPaymentDay).strip()

            strClientSignature = self.request.get('vstrClientSignature')
            strClientSignature = strClientSignature.strip()

            strEmployeeSignature = self.request.get('vstrEmployeeSignature')
            strEmployeeSignature = strEmployeeSignature.strip()

            strPremiumCalculated = self.request.get('vstrTotalPremium')


            today = datetime.datetime.today()
            today = today.date()

            thisMonth = today.month
            thisYear = today.year

            if thisMonth == 12:
                thisMonth = 1
                thisYear = today.year + 1
            else:
                thisMonth = thisMonth + 1

            thisDay = int(strPaymentDay)

            strFirstPremiumDate = datetime.date(year=thisYear, month=thisMonth, day=thisDay)


            thisPolicy = Policy()
            findRequest = Covers.query(Covers.strCoverType == "Extended")
            thisCover = findRequest.fetch()

            if len(thisCover) > 0:
                thisCover = thisCover[0]
            else:
                thisCover = Covers()

            findRequest = Policy.query(Policy.strPolicyNum == strPolicyNum)
            thisPolicyList = findRequest.fetch()

            if len(thisPolicyList) > 0:
                thisPolicy = thisPolicyList[0]

            thisPolicy.writeCoverCode(strinput=thisCover.readCoverCode())
            thisPolicy.writeFirstPremiumDate(strinput=strFirstPremiumDate)
            thisPolicy.writePaymentCode(strinput=strPolicyNum)  # Payment Transactions Code
            thisPolicy.writeReference(strinput=Guser.user_id())
            thisPolicy.writePolicyNum(strinput=strPolicyNum)
            thisPolicy.writePlanChoice(strinput=strFamilyPlanChoice)
            thisPolicy.writeExtendedPlanChoice(strinput=strExtendedPlanChoice)
            thisPolicy.writeTotalPremiums(strinput=strPremiumCalculated)
            thisPolicy.writePaymentDay(strinput=strPaymentDay)
            thisPolicy.writeClientSignature(strinput=strClientSignature)
            thisPolicy.writeEmployeeSignature(strinput=strEmployeeSignature)
            thisPolicy.put()

            self.response.write("Policy Created and SAVED")
        else:
            self.response.write("Policy not Saved")


class FuneralCoverCreatePaymentDetailsHandler(webapp2.RequestHandler):
    """
        class PhotoUploadHandler(blobstore_handlers.BlobstoreUploadHandler):
            def post(self):
                try:
                    upload = self.get_uploads()[0]
                    user_photo = UserPhoto(
                        user=users.get_current_user().user_id(),
                        blob_key=upload.key())
                    user_photo.put()

                    self.redirect('/view_photo/%s' % upload.key())

                except:
                    self.error(500)


        class ViewPhotoHandler(blobstore_handlers.BlobstoreDownloadHandler):
            def get(self, photo_key):
                if not blobstore.get(photo_key):
                    self.error(404)
                else:
                    self.send_blob(photo_key)

    """
    def get(self):
        self.response.write("Updating Debit Order Details")
        Guser = users.get_current_user()
        strBankName = self.request.get('vstrBankName')
        strBranchCode = self.request.get('vstrBranchCode')
        strAccountType = self.request.get('vstrAccountType')
        strAccountHolder = self.request.get('vstrAccountHolder')
        strAccountNumber = self.request.get('vstrAccountNumber')
        strPrincipalMemberDebitSignature = self.request.get('vstrPrincipalMemberDebitSignature')
        strDebitDateSigned = self.request.get('vstrDebitDateSigned')
        strSignedDebitOrderDocs = self.request.get('vstrSignedDebitOrderDocs')

        findRequest = WorkingPolicy.query(WorkingPolicy.strReference == Guser.user_id())
        WorkingPolList = findRequest.fetch()

        if len(WorkingPolList) > 0:
            Working = WorkingPolList[0]



        findRequest = DebitOrder.query(DebitOrder.strPolicyNum == Working.strPolicyNum)
        DebitOrderList = findRequest.fetch()

        if len(DebitOrderList) > 0:
            Debit = DebitOrderList[0]
            Debit.writePolicyNumber(strinput=Working.strPolicyNum)
            Debit.writeBankName(strinput=strBankName)
            Debit.writeBranchCode(strinput=strBranchCode)
            Debit.writeAccountType(strinput=strAccountType)
            Debit.writeAccountNumber(strinput=strAccountNumber)
            Debit.writeAccountHolder(strinput=strAccountHolder)
            Debit.writeSignedAuthorisation(strinput=strSignedDebitOrderDocs)
            Debit.put()
        else:
            Debit = DebitOrder()
            Debit.writePolicyNumber(strinput=Working.strPolicyNum)
            Debit.writeBankName(strinput=strBankName)
            Debit.writeBranchCode(strinput=strBranchCode)
            Debit.writeAccountType(strinput=strAccountType)
            Debit.writeAccountNumber(strinput=strAccountNumber)
            Debit.writeAccountHolder(strinput=strAccountHolder)
            Debit.writeSignedAuthorisation(strinput=strSignedDebitOrderDocs)
            Debit.put()

        self.response.write("...Update Completed")


class FuneralRemoveChildBYIDNumberHandler(webapp2.RequestHandler):
    def post(self):
        Guser = users.get_current_user()

        if Guser:
            strPolicyNumber = self.request.get('vstrPolicyNumber')
            strChildIDNumber = self.request.get('vstrIDNumber')

            findRequest = ChildrenDetails.query(ChildrenDetails.strIDNumber == strChildIDNumber)
            ChildList = findRequest.fetch()

            Child = ChildrenDetails()


            if len(ChildList) > 0:
                Child = ChildList[0]
                if Child.strPolicyNum == strPolicyNumber:
                    Child.key.delete()

                    template = template_env.get_template('templates/dynamic/funeralpolicy/RemoveStatus.html')
                    Context = {'RemoveStatus': "Child Removed From Policy : " + str(strPolicyNumber) + " ---- " + str(strChildIDNumber)}
                    self.response.write(template.render(Context))




class FuneralRemoveSpouseByIDNumberHandler(webapp2.RequestHandler):
    def post(self):
        Guser = users.get_current_user()

        if Guser:
            strPolicyNumber = self.request.get('vstrPolicyNumber')
            strSpouseIDNumber = self.request.get('vstrIDNumber')


            findRequest = Spouses.query(Spouses.strIDNumber == strSpouseIDNumber)
            SpouseList = findRequest.fetch()

            Spouse = Spouses()

            if len(SpouseList) > 0:
                Spouse = SpouseList[0]
                if Spouse.strPolicyNum == strPolicyNumber:
                    Spouse.key.delete()


                    template = template_env.get_template('templates/dynamic/funeralpolicy/RemoveStatus.html')
                    Context = {'RemoveStatus': "Spouse Removed From Policy : " + str(strPolicyNumber) + " ---- " + str(strSpouseIDNumber)}
                    self.response.write(template.render(Context))



class FuneralRemoveExtendedByIDNumberHandler(webapp2.RequestHandler):
    def post(self):
        Guser = users.get_current_user()

        if Guser:
            strPolicyNumber = self.request.get('vstrPolicyNumber')
            strExtendedIDNumber = self.request.get('vstrIDNumber')


            findRequest = ExtendedFamily.query(ExtendedFamily.strIDNumber == strExtendedIDNumber)

            ExtendedList = findRequest.fetch()

            Extended = ExtendedFamily()

            if len(ExtendedList) > 0:
                Extended = ExtendedList[0]
                if Extended.strPolicyNum == strPolicyNumber:
                    Extended.key.delete()


                    template = template_env.get_template('templates/dynamic/funeralpolicy/RemoveStatus.html')
                    Context = {'RemoveStatus': "Spouse Removed From Policy : " + str(strPolicyNumber) + " ---- " + str(strExtendedIDNumber)}
                    self.response.write(template.render(Context))


class FuneralRemoveBeneficiaryHandler(webapp2.RequestHandler):
    def post(self):
        Guser =  users.get_current_user()

        if Guser:
            strPolicyNumber = self.request.get('vstrPolicyNumber')
            strBeneficiaryIDNumber = self.request.get('vstrIDNumber')

            findRequest = Beneficiary.query(Beneficiary.strIDNumber == strBeneficiaryIDNumber)
            BeneficiaryList = findRequest.fetch()

            if len(BeneficiaryList) > 0:
                Benefitor = BeneficiaryList[0]
                if Benefitor.strPolicyNum == strPolicyNumber:
                    Benefitor.key.delete()


                    template = template_env.get_template('templates/dynamic/funeralpolicy/RemoveStatus.html')
                    Context = {'RemoveStatus': "Spouse Removed From Policy : " + str(strPolicyNumber) + " ---- " + str(strBeneficiaryIDNumber)}
                    self.response.write(template.render(Context))


class PaymentDetailsPayrollUploadFormHandler(webapp2.RequestHandler):
    def get(self):
        upload_url = blobstore.create_upload_url('/upload_docs')
        # To upload files to the blobstore, the request method must be "POST"
        # and enctype must be set to "multipart/form-data".
        self.response.out.write("""
                <html><body>
                <form action="{0}" method="POST" enctype="multipart/form-data">
                  Upload File: <input type="file" name="file"><br>
                  <input type="submit" name="submit" value="Submit">
                </form>
                </body></html>
                                """.format(upload_url))






class FuneralCoverTermsHandler(webapp2.RequestHandler):
    def get(self):
        template = template_env.get_template('templates/dynamic/covers/terms.html')
        Context = {}
        self.response.write(template.render(Context))


class FuneralCoverDetailHandler(webapp2.RequestHandler):
    def get(self):
        URL = self.request.url
        URLlist = URL.split("/")
        strPolicyNum = URLlist[len(URLlist) - 1]

        findRequest = Policy.query(Policy.strPolicyNum == strPolicyNum)
        PolicyList = findRequest.fetch()

        if len(PolicyList) > 0:
            thisPolicy = PolicyList[0]

            # strPaymentMethod = ndb.StringProperty() # Direct Deposit , Payroll , Debit Order, Persal Deduction, Intermediary, Declaration

            if thisPolicy.readPaymentMethod() == "Direct Deposit":
                findRequest = DirectDeposit.query(DirectDeposit.strPolicyNum == thisPolicy.readPolicyNum())
                PaymentDetailsList = findRequest.fetch()

                PaymentDetailsList  = findRequest.fetch()
            elif thisPolicy.readPaymentMethod() == "Debit Order":
                findRequest = DebitOrder.query(DebitOrder.strPolicyNum == thisPolicy.readPolicyNum())
                PaymentDetailsList = findRequest.fetch()
            else:
                PaymentDetailsList = []
        else:
            thisPolicy = Policy()
            PaymentDetailsList = []



        findRequest = ClientsPersonalDetails.query(ClientsPersonalDetails.strPolicyNum == strPolicyNum)
        PrincipalMemberList = findRequest.fetch()

        findRequest = ClientsResidentialAddress.query(ClientsResidentialAddress.strPolicyNum == strPolicyNum)
        ResidentialList = findRequest.fetch()

        findRequest = ClientsPostalAddress.query(ClientsPostalAddress.strPolicyNum == strPolicyNum)
        PostalAddressList = findRequest.fetch()

        findRequest = ClientsContactDetails.query(ClientsContactDetails.strPolicyNum == strPolicyNum)
        ContactList = findRequest.fetch()

        findRequest = ChildrenDetails.query(ChildrenDetails.strPolicyNum == strPolicyNum)
        ChildrenList = findRequest.fetch()

        findRequest = Spouses.query(Spouses.strPolicyNum == strPolicyNum)
        SpousesList = findRequest.fetch()

        findRequest = ExtendedFamily.query(ExtendedFamily.strPolicyNum == strPolicyNum)
        ExtendedFamilyList = findRequest.fetch()

        findRequest = Beneficiary.query(Beneficiary.strPolicyNum == strPolicyNum)
        BeneficiaryList = findRequest.fetch()

        findRequest = PaymentHistory.query(PaymentHistory.strPaymentCode == thisPolicy.strPolicyNum).order(PaymentHistory.strDatePaymentMade)
        TransactionList = findRequest.fetch()


        template = template_env.get_template('templates/dynamic/covers/coverdetail.html')
        Guser = users.get_current_user()

        if users.is_current_user_admin():
            IsAdmin = "YES"
        else:
            IsAdmin = "NO"
        Context = {'IsAdmin': IsAdmin, 'PrincipalMember': PrincipalMemberList, 'ResidentialList': ResidentialList, 'PostalAddressList': PostalAddressList, 'ContactList': ContactList,
                   'ChildrenList': ChildrenList, 'SpousesList': SpousesList, 'ExtendedList': ExtendedFamilyList, 'BeneficiaryList': BeneficiaryList,
                   'PaymentDetailsList': PaymentDetailsList, 'PaymentMethod': thisPolicy.readPaymentMethod(),'thisPolicy': thisPolicy, 'TransactionsList': TransactionList}
        self.response.write(template.render(Context))


class FuneralCoverProcessPayment(webapp2.RequestHandler):
    def get(self):
        strPolicyNumber = self.request.get('vstrPolicyNumber')
        logging.info(strPolicyNumber)
        strPaymentAmount = self.request.get('vstrPaymentAmount')
        logging.info(strPaymentAmount)
        strNotification = str(self.request.get('strPaymentNotification'))
        strPayMonthsList = self.request.get('vstrPayMonthsList')

        strPayMonthsList = strPayMonthsList
        strPayMonthsList = strPayMonthsList.strip(",")



        tempArray = []
        tString = ""
        tcount = 1
        for tc in strPayMonthsList:
            if tcount > 3:
                tempArray.append(tString)
                tcount = 1
                tString = ""
            else:
                tString = tString + tc
                tcount = tcount + 1
        tempArray.append(tString)


        strPayMonthsList = tempArray

        SMSbox = SMS()
        EmailBox = Emails()
        FormattedMessage = "Payment for Midey Funeral Policy Number : " + strPolicyNumber + " was received"

        if strNotification.isdigit():
            SMSbox.sendSMS(strCell=strNotification,strMessage=FormattedMessage)
        elif "@" in strNotification:
            EmailBox.sendEmailNotification(strEmail=strNotification,strSubject="Midey Funeral Payment Notifications",strMessage=FormattedMessage)
        else:
            pass

        self.response.write("Payment Processing...")

        findRequest = Policy.query(Policy.strPolicyNum == strPolicyNumber)
        PolicyList = findRequest.fetch()


        if len(PolicyList) > 0:
            thisPolicy = PolicyList[0]
        else:
            thisPolicy = Policy()


        thisPolicy.writePaymentCode(strinput=thisPolicy.readPolicyNum())
        thisPolicy.put()

        findRequest = PaymentHistory.query()
        PaymentList = findRequest.fetch()
        payindex = len(PaymentList)


        findRequest = PaymentHistory.query(PaymentHistory.strPaymentCode == strPolicyNumber).order(PaymentHistory.strDatePaymentMade)
        PaymentList = findRequest.fetch()


        strPaymentAmount = str(strPaymentAmount)

        tc = 0
        for m in strPayMonthsList:
            tc = tc + 1

        logging.info(str(tc))
        if strPaymentAmount.isdigit():
            strPaymentAmount = int(strPaymentAmount)
            AtomicPaymentAmount = strPaymentAmount/len(strPayMonthsList)
            logging.info("PLEASE CHECK THIS AMOUNT : " + str(AtomicPaymentAmount) + "COMPARE TO THE DIVISOR : " + str(len(strPayMonthsList)))
        else:
            AtomicPaymentAmount = 0

        TotalMonths = len(strPayMonthsList)

        ThisMonth = datetime.datetime.now()
        MyDate = ThisMonth.date()
        ThisMonth = MyDate.month
        ThisYear = MyDate.year


        if TotalMonths > (12 - ThisMonth):
            FinalYear = ThisYear + 1

        Count = 0
        for Month in strPayMonthsList:
            Payment = PaymentHistory()
            Payment.writePaymentsCode(strinput=strPolicyNumber)

            Payment.writeIndex(strinput=payindex)
            payindex = payindex + 1
            Payment.strDatePaymentMade = datetime.datetime.now()
            Payment.writePaymentMethod(strinput="cash")
            logging.info("Months About to Be written to the System : " + Month)
            logging.info(" -- ")
            Payment.writePayForMonth(strinput=Month)
            Payment.writePaymentAmount(strinput=AtomicPaymentAmount)
            if Count <= (12 - ThisMonth):
                Payment.writePayYear(strinput=ThisYear)
                Count = Count + 1
            else:
                Payment.writePayYear(strinput=FinalYear)
                ThisYear = FinalYear
                Count = 0
            Payment.put()











        self.response.write("Payment Processing Complete...")


class FuneralCreateHandler(webapp2.RequestHandler):
    def get(self):
        try:
            Guser = users.get_current_user()
            if Guser:
                findRequest = WorkingPolicy.query(WorkingPolicy.strActivated == False, WorkingPolicy.strReference == Guser.user_id())
                WorkingPols = findRequest.fetch()

                logging.info("Working Pols")

                for Working in WorkingPols:
                    Working.strActivated = True
                    Working.put()

            logging.info("Working Pols Finally")

            self.redirect("/employees/funeral-cover")

        except:
            pass



class FuneralCoverEditPolicy(webapp2.RequestHandler):
    def get(self):

        Guser = users.get_current_user()
        if Guser:

            vstrPolicyNumber = self.request.get('vstrPolicyNumber')

            findRequest = WorkingPolicy.query()
            WorkingList = findRequest.fetch()


            for Working in WorkingList:
                Working.strActivated = True
                Working.put()

            findRequest = WorkingPolicy.query(WorkingPolicy.strReference == Guser.user_id())
            CountList = findRequest.fetch()
            CountList = len(CountList)

            Working = WorkingPolicy()
            Working.writeReference(strinput=Guser.user_id())
            Working.writePolicyNum(strinput=vstrPolicyNumber)

            Working.writeTotalCreated(strinput=CountList + 1)
            Working.writeActivated(strinput=False)
            Working.put()

            self.response.write("""
                                Succesfully reactivated Policy : """ + vstrPolicyNumber + """ For editing please click here to <a href="/employees/funeral-cover"><strong>Edit Your Policy</strong></a>

                                """)

        else:
            pass


class FuneralDeletePolicy(webapp2.RequestHandler):
    def get(self):
        vstrPolicyNumber = self.request.get('vstrPolicyNumber')
        try:
            findRequest = Policy.query(Policy.strPolicyNum == vstrPolicyNumber)
            PolicyList = findRequest.fetch()

            for Pol in PolicyList:
                Pol.key.delete()

            findRequest = ClientsPersonalDetails.query(ClientsPersonalDetails.strPolicyNum == vstrPolicyNumber)
            clientList = findRequest.fetch()

            for client in clientList:
                client.key.delete()

            findRequest = ClientsContactDetails.query(ClientsContactDetails.strPolicyNum == vstrPolicyNumber)
            ContactList = findRequest.fetch()

            for contact in ContactList:
                contact.key.delete()

            findRequest = ClientsResidentialAddress.query(ClientsResidentialAddress.strPolicyNum == vstrPolicyNumber)
            ResidentialList = findRequest.fetch()

            for Residential in ResidentialList:
                Residential.key.delete()

            findRequest = ClientsPostalAddress.query(ClientsPostalAddress.strPolicyNum == vstrPolicyNumber)
            PostalAddressList = findRequest.fetch()

            for postal in PostalAddressList:
                postal.key.delete()

            findRequest = Beneficiary.query(Beneficiary.strPolicyNum == vstrPolicyNumber)
            BeneficiaryList = findRequest.fetch()

            for Benefactor in BeneficiaryList:
                Benefactor.key.delete()


            findRequest = ChildrenDetails.query(ChildrenDetails.strPolicyNum == vstrPolicyNumber)
            ChildList = findRequest.fetch()

            for child in ChildList:
                child.key.delete()

            findRequest = Spouses.query(Spouses.strPolicyNum == vstrPolicyNumber)
            SpouseList = findRequest.fetch()

            for Spouse in SpouseList:
                Spouse.key.delete()

            findRequest = ExtendedFamily.query(ExtendedFamily.strPolicyNum == vstrPolicyNumber)
            ExtendedList = findRequest.fetch()

            for Extended in ExtendedList:
                Extended.key.delete()


            findRequest = PaymentHistory.query(PaymentHistory.strPaymentCode == vstrPolicyNumber)
            PaymentHistoryList = findRequest.fetch()

            for payment in PaymentHistoryList:
                payment.key.delete()

            findRequest = Claims.query(Claims.strPolicyNum == vstrPolicyNumber)
            ClaimList =  findRequest.fetch()

            for claim in ClaimList:
                claim.key.delete()

            findRequest = DirectDeposit.query(DirectDeposit.strPolicyNum == vstrPolicyNumber)
            DirectDepositList = findRequest.fetch()

            for direct in DirectDepositList:
                direct.key.delete()

            findRequest = Cash.query(Cash.strPolicyNum == vstrPolicyNumber)
            CashList = findRequest.fetch()

            for casher in CashList:
                casher.key.delete()

            findRequest = DebitOrder.query(DebitOrder.strPolicyNum == vstrPolicyNumber)
            DebitList = findRequest.fetch()

            for debit in DebitList:
                debit.key.delete()

            # We cant delete Working Policy List because it will disturb the creation of Policy Numbers

            self.response.write(

                """Policy : """ + vstrPolicyNumber +
                """
                is completely removed and all records associated with that policy, <a href="/employees/funeral-cover"><strong>Please Click Here To Continue</strong></a>
                """)

        except:
            self.response.write("There was an error Deleting Policy : " + vstrPolicyNumber + " the policy might not be completely removed")

class FuneralCalPremiumHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write("""

        <strong class="label-success">Total Premiums Calculated</strong>

        """)

class FuneralCoverClaim(webapp2.RequestHandler):
    def get(self):
        Guser = users.get_current_user()
        self.response.write("Claim Processing....")
        vstrPolicyNumber = self.request.get("vstrPolicyNumber")
        vstrClaimantIDNumber = self.request.get("vstrClaimantIDNumber")

        findRequest = ClientsPersonalDetails.query(ClientsPersonalDetails.strIDNumber == vstrClaimantIDNumber)
        ClientsList = findRequest.fetch()

        ClaimantDetails = None
        ExtendedChoice = False
        FamilySingle = False
        ItsChild = False
        if len(ClientsList) > 0:
            ClaimantDetails = ClientsList[0]
            FamilySingle = True


        findRequest = Spouses.query(Spouses.strIDNumber == vstrClaimantIDNumber)
        SpousesList = findRequest.fetch()

        if len(SpousesList) > 0:
            ClaimantDetails = SpousesList[0]
            FamilySingle = True

        findRequest = ChildrenDetails.query(ChildrenDetails.strIDNumber == vstrClaimantIDNumber)
        ChildrenList = findRequest.fetch()

        if len(ChildrenList) > 0:
            ClaimantDetails = ChildrenList[0]
            FamilySingle = True
            ItsChild = True

        findRequest = ExtendedFamily.query(ExtendedFamily.strIDNumber == vstrClaimantIDNumber)
        ExtendedList = findRequest.fetch()

        if len(ExtendedList) > 0:
            ClaimantDetails = ExtendedList[0]
            ExtendedChoice = True



        if not(ClaimantDetails == None):

            if ClaimantDetails.strPolicyNum == vstrPolicyNumber:

                Claim = Claims()
                Claim.writeReference(strinput=Guser.user_id())
                Claim.writeClaimForID(strinput=vstrClaimantIDNumber)
                Claim.writePolicyNum(strinput=vstrPolicyNumber)
                Claim.writeNames(ClaimantDetails.strFullNames)
                Claim.writeClaimStatus(strinput="Not Processed")
                Claim.writeRelationship(strinput=ClaimantDetails.strRelationship)
                Claim.writeSurname(ClaimantDetails.strSurname)
                Claim.writeDateOfBirth(ClaimantDetails.strDateOfBirth)
                Claim.writeTitle(ClaimantDetails.strTitle)
                Claim.writeNationality(ClaimantDetails.strNationality)
                findRequest = Policy.query(Policy.strPolicyNum == vstrPolicyNumber)
                PolicyList = findRequest.fetch()
                age = num_years(begin=Claim.strDateOfBirth)
                if len(PolicyList) > 0:
                    ClaimPolicy = PolicyList[0]
                    if (FamilySingle == True) and (ItsChild == True):

                        if ClaimPolicy.strPlanChoice == "A":
                            if (age >= 1) and (age <= 5):
                                Claim.writeClaimAmount(strinput=2000)
                            if (age >= 6) and (age <= 12):
                                Claim.writeClaimAmount(strinput=2500)
                            if (age >= 13) and (age <= 21):
                                Claim.writeClaimAmount(strinput=3000)

                            if age == 0:
                                Claim.writeClaimAmount(strinput=1000)

                        elif ClaimPolicy.strPlanChoice == "B":
                            if (age >= 1) and (age <= 5):
                                Claim.writeClaimAmount(strinput=2800)
                            if (age >= 6) and (age <= 12):
                                Claim.writeClaimAmount(strinput=3000)
                            if (age >= 13) and (age <= 21):
                                Claim.writeClaimAmount(strinput=3500)

                            if age == 0:
                                Claim.writeClaimAmount(strinput=1000)

                        elif ClaimPolicy.strPlanChoice == "C":
                            if (age >= 1) and (age <= 5):
                                Claim.writeClaimAmount(strinput=4000)
                            if (age >= 6) and (age <= 12):
                                Claim.writeClaimAmount(strinput=4500)
                            if (age >= 13) and (age <= 21):
                                Claim.writeClaimAmount(strinput=5000)

                            if age == 0:
                                Claim.writeClaimAmount(strinput=1200)

                        elif ClaimPolicy.strPlanChoice == "D":
                            if (age >= 1) and (age <= 5):
                                Claim.writeClaimAmount(strinput=5000)
                            if (age >= 6) and (age <= 12):
                                Claim.writeClaimAmount(strinput=5500)
                            if (age >= 13) and (age <= 21):
                                Claim.writeClaimAmount(strinput=6500)

                            if age == 0:
                                Claim.writeClaimAmount(strinput=1500)
                    elif (FamilySingle == True) and not(ExtendedChoice):
                        if ClaimPolicy.strPlanChoice == "A":

                            if (age >= 18) and (age <= 60):
                                Claim.writeClaimAmount(strinput=5000)

                        elif ClaimPolicy.strPlanChoice == "B":
                            if (age >= 18) and (age <= 60):
                                Claim.writeClaimAmount(strinput=7000)
                        elif ClaimPolicy.strPlanChoice == "C":
                            if (age >= 18) and (age <= 60):
                                Claim.writeClaimAmount(strinput=10000)
                        elif ClaimPolicy.strPlanChoice == "D":
                            if (age >= 18) and (age <= 60):
                                Claim.writeClaimAmount(strinput=12000)
                        elif ClaimPolicy.strSinglePlanChoice == "A":
                            Claim.writeClaimAmount(strinput=5000)
                        elif ClaimPolicy.strSinglePlanChoice == "B":
                            Claim.writeClaimAmount(strinput=7000)
                        elif ClaimPolicy.strSinglePlanChoice == "C":
                            Claim.writeClaimAmount(strinput=10000)
                        elif ClaimPolicy.strSinglePlanChoice == "D":
                            Claim.writeClaimAmount(strinput=12000)
                    elif ExtendedChoice:
                        if ClaimPolicy.strExtendedPlanChoice == "A":
                            Claim.writeClaimAmount(strinput=5000)
                        elif ClaimPolicy.strExtendedPlanChoice == "B":
                            Claim.writeClaimAmount(strinput=7000)
                        elif ClaimPolicy.strExtendedPlanChoice == "C":
                            Claim.writeClaimAmount(strinput=10000)
                        elif ClaimPolicy.strExtendedPlanChoice == "D":
                            Claim.writeClaimAmount(strinput=12000)
                Claim.put()
                self.response.write("Claim processed fully ...Please check the claims dialog for further processing")
            else:
                self.response.write("Claim Processing failed to complete- Claimant ID Number dont match the Policy Number")
        else:
            self.response.write("Claim Processing failed to complete- Claimant Details not found")




app = webapp2.WSGIApplication([
    ('/funeral/create/family', FuneralCoverCreateFamilyHandler),
    ('/funeral/create/single', FuneralCoverCreateSingleHandler),
    ('/funeral/create/extended', FuneralCoverCreateExtendedHandler),
    ('/funeral/create/paymentdetails',FuneralCoverCreatePaymentDetailsHandler),
    ('/funeral-cover/remove/child',FuneralRemoveChildBYIDNumberHandler),
    ('/funeral-cover/remove/spouse',FuneralRemoveSpouseByIDNumberHandler),
    ('/funeral-cover/remove/extended', FuneralRemoveExtendedByIDNumberHandler),
    ('/funeral-cover/remove/beneficiary', FuneralRemoveBeneficiaryHandler),
    ('/funeral/paymentdetails/dynupload', PaymentDetailsPayrollUploadFormHandler),
    ('/funeral-cover/terms', FuneralCoverTermsHandler),
    ('/funeral-cover/client/processpayment', FuneralCoverProcessPayment),
    ('/funeral-cover/client/.*', FuneralCoverDetailHandler),
    ('/funeral/create', FuneralCreateHandler),
    ('/funeral-cover/editpolicy', FuneralCoverEditPolicy),
    ('/funeral-cover/deletepolicy',FuneralDeletePolicy),
    ('/funeral-cover/calpremium', FuneralCalPremiumHandler),
    ('/funeral-cover/claim', FuneralCoverClaim)


], debug=True)

