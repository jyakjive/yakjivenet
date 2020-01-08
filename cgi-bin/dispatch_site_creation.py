#!D:/Python27/python.exe
##!/usr/bin/python

########
# Copyright (c) 2006 Christopher Jerome Andrews
########

#imports
import os
import util.exceptions
from ui.mvc import *
from admin.mvc_admin import *
import cgi
from admin.vars import *
#import logging

#declarations

DEBUG = False

util.exceptions.handleExceptions()

form = cgi.FieldStorage()

nextPage = DEFAULT_REDIRECT
model = None
try:
    model = AdminModel(form)
    check = model.validate()
    if (check):
        for bo in model.getBusinessObjects():
            newBo = bo(model, None)
            newBo.execute()

        nextPage = model.getRouter(form).getRoute()
except ModelError, e:
    # TODO: implement exception handling
    raise e
except RouterError, e:
    # TODO: implement exception handling
    raise e

#raise str(model.operation + '<br>\n' + str(model.step) + '<br>\n' + nextPage + '<br>\n' + model.toQueryString())

if (DEBUG):
    if (model.errorMessage != ''):
        raise str('DEBUG MODE: ' + model.errorMessage) + ' \n<br>' + nextPage

#Redirecting to the select page
if (model.useForward):
    if ((model is not None) and (nextPage != DEFAULT_REDIRECT)):
        data = model.toQueryString()
        if (data != ''):
            data += '&'

        #raise nextPage + '?' + data

        doForward(nextPage, ROOT_SITE_ADMIN_URL, data)
    else:
        doForward(nextPage, ROOT_SITE_ADMIN_URL)
else:
    doRedirect(nextPage)
