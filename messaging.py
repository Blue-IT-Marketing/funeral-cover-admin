import os
import webapp2
import jinja2
from google.appengine.ext import ndb
from google.appengine.api import users
import logging
template_env = jinja2.Environment(
loader=jinja2.FileSystemLoader(os.getcwd()))

from Employee import *


class Messages(ndb.Expando):
    strEmployeeCode = ndb.StringProperty()
    strMessageHeading = ndb.StringProperty()
    strMessageBody =ndb.StringProperty()
    strMessageFromReference = ndb.StringProperty()

    def writeMessageHeading(self,strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if not(strinput == None):
                self.strMessageHeading = strinput
                return True
            else:
                return False
        except:
            return False

    def writeMessageBody(self,strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if not (strinput == None):
                self.strMessageBody = strinput
                return True
            else:
                return False
        except:
            return False

    def writeMessageFromReference(self,strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if not (strinput == None):
                self.strMessageFromReference = strinput
                return True
            else:
                return False
        except:
            return False

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


class SendMessagingHandler(webapp2.RequestHandler):
    def post(self):
        try:
            Guser = users.get_current_user()

            strEmployeeCode = self.request.get('vstrEmployeeCode')
            strMessageHeading = self.request.get('vstrSubject')
            strMessageBody = self.request.get('vstrMessageBody')

            Employee = EmploymentDetails()
            Message = Messages()

            findRequest = EmploymentDetails.query(EmploymentDetails.strEmployeeCode == strEmployeeCode)
            TempEmployeeList = findRequest.fetch()

            if len(TempEmployeeList) > 0:
                Employee = TempEmployeeList[0]
            else:
                self.redirect('/admin')


            Employee.strTotalMessages = Employee.strTotalMessages + 1
            Employee.put()

            Message.writeEmployeeCode(strinput=strEmployeeCode)
            Message.writeMessageBody(strinput=strMessageBody)
            Message.writeMessageHeading(strinput=strMessageHeading)
            Message.writeMessageFromReference(strinput=Guser.user_id())

            Message.put()

            self.redirect('/admin')

        except:
            self.redirect('/admin')











app = webapp2.WSGIApplication([
    ('/admin/employees/messaging', SendMessagingHandler )
], debug=True)


