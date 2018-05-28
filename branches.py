import os
import webapp2
import jinja2
from google.appengine.ext import ndb
from google.appengine.api import users
import logging
template_env = jinja2.Environment(
loader=jinja2.FileSystemLoader(os.getcwd()))

from database import Constants,BranchDetails


class BranchesHandler(webapp2.RequestHandler):

    def get(self):
        logging.info("Branches Handler Calleds")
        URL = str(self.request.url)

        URLList = URL.split("/")
        BranchCode = URLList[len(URLList) - 1]

        if not(BranchCode == None):
            findRequest = BranchDetails.query(BranchDetails.strCompanyBranchCode == BranchCode)
            results = findRequest.fetch()
            branchdet = BranchDetails()
            if len(results) > 0:
                branchdet = results[0]
                logging.info("FOUND Branch")

            context = {'vstrBranchName': branchdet.readCompanyBranchName(),
                       'vstrBranchCode': branchdet.readCompanyBranchCode(),
                       'vstrBranchAddress': branchdet.readCompanyBranchAddress(),
                       'vstrBranchContact': branchdet.readCompanyBranchTel(),
                       'vstrBranchManager': branchdet.readBranchManagerName(),
                       'vstrBranchManagerContact': branchdet.readBrachManagerTel(),
                       'vstrBranchManagerEmail': branchdet.readBranchManagerEmail(),
                       'vstrBranchEmail': branchdet.readCompanyBranchEmail()}
            template = template_env.get_template('templates/dynamic/admin/BranchDetails.html')

            self.response.write(template.render(context))
        else:
            logging.info(msg="Not Found from URL")
    




app = webapp2.WSGIApplication([
    ('/admin/branch/.*',BranchesHandler)
], debug=True)


