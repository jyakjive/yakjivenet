# imports

import os
import cgi
import time
from newscommunity.ncvars import *
from newscommunity.application import *
from classes.newspage_handler import *
from util.user_management import *
from classes.section_handler import *
from ui.mvc import *
from util.email import *
from ui.os_extras import checkReferer

# declarations

OP_CONTACT_FORM = 'contact_form'

SUBJECT_PREFACE = 'Web submission --'

# classes

class MailModel(Model):
    ''' This is not a 'male model,' but rather the data object
        that captures the information coming in from a web form
        submission for a YJ contact page.
    '''

    def __init__(self, form):
        ''' Constructor. '''
        Model.__init__(self, form)
        # Order is important!
        self.businessObjects = [
            FormMailBO]

    def getRouter(self, form = None):
        ''' Get the Router object that will direct the flow of the
            user's interaction with the mail system.
        '''
        return MailRouter(form, self)

    def validate(self):
        ''' Check to see if the object contains the necessary information
            to process the mail request.
        '''
        #raise str(repr(self.__dict__))
        check = 'operation' in self.__dict__
        if (not check):
            self.errorMessage += 'Failed to find operation\n<br>'

        check = check and checkReferer(APPLICATION.rootURL, True)
        if (not check):
            self.errorMessage += 'Failed referer\n<br>'

        if (check):
            if (OP_CONTACT_FORM in self.operation):
                check = check and ('fromEmail' in self.__dict__)
                if (not check):
                    self.errorMessage += '1'
                check = check and ('fromName' in self.__dict__)
                if (not check):
                    self.errorMessage += '2'
                check = check and ('subject' in self.__dict__)
                if (not check):
                    self.errorMessage += '3'
                check = check and ('content' in self.__dict__)
                if (not check):
                    self.errorMessage += '4'
                check = check and ('redirect' in self.__dict__)
                if (not check):
                    self.errorMessage += '5'
                if ('content' not in self.__dict__):
                    self.__dict__['content'] = 'Not found'
                check = check and (self.subject.find(SUBJECT_PREFACE) == 0)
                if (not check):
                    self.errorMessage += '6'

                if ('contact' not in self.__dict__):
                    self.__dict__['contact'] = 'No'

            else:
                check = False
        return check

class MailRouter(FormRouter):
    ''' Class used to route mail submissions. '''
    def validate(self):
        ''' Make sure the Router has the correct information. '''
        check = FormRouter.validate(self)
        check = check and (self.model.operation != '')
        if (not check):
            self.model.errorMessage = '7'
        return check

    def getRoute(self):
        ''' Get the next web page.
            Returns the name of the web page.
        '''
        redir = APPLICATION.redirectOnFailedLogin
        if (self.validate()):
            if (self.model.operation == OP_CONTACT_FORM):
                if (self.model.errorMessage == ''):
                    redir = self.model.redirect
                else:
                    redir = APPLICATION.rootURL

        return redir

class FormMailBO(BusinessObject):
    ''' Business object used to process form mail submissions.'''
    def execute(self):
        ''' Send the email. Does not return a fatal error if there
            has been a failure while attempting to send mail.
        '''
        if ((self.model.operation == OP_CONTACT_FORM) and
                (self.model.errorMessage == '')):

            emailDict = dict()
            emailDict['content'] = self.model.content
            emailDict['contact'] = self.model.contact
            emailDict['fromName'] = self.model.fromName
            emailDict['fromEmail'] = self.model.fromEmail
            emailDict['toEmail'] = APPLICATION.contactEmail
            emailDict['subject'] = self.model.subject
            timestr = time.strftime('%d %b %Y %H:%M:%S +0000', time.gmtime(time.time()))
            emailDict['date'] = timestr

            emailBody = readTextFile(FILENAME_EMAIL_CONTACT, True, emailDict)

            try:
                sendEmail(self.model.fromEmail, APPLICATION.contactEmail, emailBody)
            except Exception, e:
                self.model.errorMessage = '8'