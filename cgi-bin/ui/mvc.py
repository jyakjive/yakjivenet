# imports

import os
from cgi import *
import urllib2
import sys

MIME_TEXT_PLAIN = 'text/html'
MIME_TEXT_XML = 'text/xml'
MIME_TEXT_CSV = 'text/csv'
MIME_TEXT_CSS = 'text/css'
MIME_IMAGE_JPG = 'image/jpg'
MIME_IMAGE_GIF = 'image/gif'
MIME_IMAGE_PNG = 'image/png'
MIME_APPLICATION_PDF = 'application/pdf'
MIME_APPLICATION_DOC = 'application/msword'

# definitions

def doForward(theURL, defaultURL, queryString=None, mimeType=MIME_TEXT_PLAIN):
    ''' Forward to the next location by loading it and passing
        the loaded data immediately to the client.

        Other mime types to use:
            image/png
            image/gif
            image/jpg
            text/plain
            text/xml
            text/csv
            text/css

        Note, if you're passing an .htm or .html page, the method
        won't attempt to pass the queryString because you'll get a 405 error.
    '''

    if ((theURL is None) or (theURL == '')):
        raise Exception('URL cannot be None or empty')

    if (theURL.find('://') == -1):
        theURL = defaultURL + theURL

    if ((queryString is not None)
            and (queryString != '')
            and ('.htm' != theURL.lower()[-4: len(theURL)])
            and ('.html' != theURL.lower()[-5: len(theURL)])):
        req = urllib2.Request(
                url=theURL,
                data=queryString)
    else:
        req = urllib2.Request(url=theURL)

    f = urllib2.urlopen(req)

    print 'Content-Type: ' + mimeType + '\n'
    sys.stdout.write(f.read())

def doRedirect(theURL, defaultURL = None):
    '''Do a simple redirect call.'''

    if (theURL.find('://') == -1):
        if (defaultURL is None):
            theURL = defaultURL + theURL
        else:
            raise ('Unable to forward to a page with no protocol.');

    print 'Location: ' + str(theURL)
    print

# classes

class ModelError(Exception):
    def __init__(self, value):
        '''Constructor.'''
        self.value = value

    def __str__(self):
        '''Return a string representation of this object.'''
        return repr(self.value)

class RouterError(Exception):
    def __init__(self, value):
        '''Constructor.'''
        self.value = value

    def __str__(self):
        '''Return a string representation of this object.'''
        return repr(self.value)

class Model:
    '''The model object encapsulates the data that will be used to process
    a client request to a script in the application.

    In this pattern, the Model contains information about the objects that
    will process it, as well as the object that will route it to the next
    page in the application.'''

    def __init__(self, form = None):
        '''Constructor.  Automatically pulls out all the form input k-v pairs as
        attributes.  Single keys will be scalar attributes, list keys will be list
        attributes.

        For example a=1&b=2&b=3 will generate a Model instance with a = 1 and b = [2,3].

        If the form is None, there will be no attributes created.

        Subclasses MUST call this constructor or implement their own mechanism
        for scraping attributes out of the form.'''
        self.form = form
        self.businessObjects = list()
        self.infoMessage = ''
        self.errorMessage = ''
        self.useForward = True

        if (form is not None):
            for key in form.keys():
                data = form.getlist(key)
                if (len(data) == 1):
                    exec('self.' + key + ' = ' + repr(data[0]))
                else:
                    exec('self.' + key + ' = data')

    def validate(self):
        '''Check the model to make sure that all the
        correct data are contained.'''
        return true

    def getBusinessObjects(self):
        '''Get the list of business objects, if any, that will be
        used to process this model.'''
        return self.businessObjects

    def getRouter(self, form = None):
        '''Get the Router object that will determine where this
        Model will be sent next in the business flow.'''
        raise ModelError('Model.getRouter() not yet implemented.')

    def toQueryString(self):
        '''Conver the Model attributes to a key-value pair query
        string that will be posted to the next URL.'''
        data = ''
        for item in self.__dict__:
            if (item in ['form', 'businessObjects']):
                continue
            if (isinstance(self.__dict__[item], list)):
                for val in self.__dict__[item]:
                    if (data != ''):
                        data += '&'
                    data += item + '=' + str(val)
            else:
                if (data != ''):
                    data += '&'
                data += item + '=' + str(self.__dict__[item])
        return data

class Router:
    '''Router objects use the state of the Model and the
    previous location information to return the next destination
    in the application.'''

    def __init__(self, form = None, model = None):
        '''Constructor.'''
        self.form = form
        if ('HTTP_REFERER' in os.environ):
            self.referer = os.environ['HTTP_REFERER']
        else:
            self.referer = 'Not Available'
        self.model = model

class FormRouter(Router):
    def validate(self):
        '''Check to make sure that all of the appropriate information is contained in the Model and state.'''
        check = (self.form is not None)
        return check

    def getRoute(self):
        '''Get the route that will be used for the given Model and state.'''
        raise RouterError('getRoute() not yet defined')

class Command:
    '''Superclass to provide a simple Commmand pattern interface.'''
    def execute(self):
        pass

class BusinessObject(Command):
    def __init__(self, model, securityInfo):
        '''Constructor.'''
        self.model = model
        self.securityInfo = securityInfo

class SecurityInfo:
    def __init__(self, user, storage, userRules = None):
        '''Constructor.'''
        self.user = user
        self.storage = storage
        self.userRules = userRules
