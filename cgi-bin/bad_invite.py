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
from util.fileutils import *

util.exceptions.handleExceptions()

form = cgi.FieldStorage()

inviteCode = form.getfirst('inviteCode')
if (inviteCode is None):
    inviteCode = 'None'

replaceDict = dict()
replaceDict['title'] = 'Unknown invitation code'
replaceDict['itemTitle'] = 'Unknown invitation code'
replaceDict['itemContent'] = '''
<p>We apologize, but the invite code you entered [''' + inviteCode + ''']
was not recognized as a valid invite code.
<p>If you would like to request
a valid invite code, please
<a href="http://www.yakjive.com/yjcontact.html">send us a message.</a>
'''

pageTemplate = readTextFile(FILENAME_PAGE_TEMPLATE, replaceDict = replaceDict)

print "Content-Type: text/html\n\n" + pageTemplate

