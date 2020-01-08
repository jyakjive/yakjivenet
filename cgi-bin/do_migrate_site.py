#!D:/Python27/python.exe
##!/usr/bin/python

#imports

from shutil import *

import cgi
import cgitb; cgitb.enable()
import Cookie
import util.exceptions
import os
from util.fileutils import log

from db.tools import *

util.exceptions.handleExceptions()
form = cgi.FieldStorage()

print "Content-Type: text/html"     # HTML is following
print                               # blank line, end of headers

redirect = 'http://www.yakjive.com'
if ((not form.has_key('password')) or (form.getfirst('password') != 'jezebel22')):
    redirect = 'http://www.yakjive.com'
    print 'Error'
elif (form.has_key('siteID') and form.has_key('siteCgiDir')):

    # Extract the form values
    siteID = form.getfirst('siteID')
    siteCgiDir = form.getfirst('siteCgiDir')

    count = form.getfirst('count')
    startAt = form.getfirst('startAt')

    if ((count is None) or (count == '')):
        count = None
    else:
        count = int(count)
    if ((startAt is None) or (startAt == '')):
        startAt = None
    else:
        startAt = int(startAt)

    print '<html><body>About to migrate site: ' + str(siteID) + ' in dir ' + siteCgiDir
    print '<hr>'

    sdc = SiteDbCreator(siteID)
    # Attempt to delete the database tables if there was a screw up
    try:
        log('About to clean up site: ' + str(siteID))
        if ((startAt is None) or (startAt == 0)):
            sdc.cleanUp()
            print 'Cleaned up <br>\n'
            log('About to execute SDC for site: ' + str(siteID))
            sdc.execute()
    except:
        print 'Cleaned up skipped <br>\n'
    log('About to migrate site: ' + str(siteID))
    report = sdc.migrate(siteCgiDir, count, startAt)

    print report

    print '</body></html>'

else:
    print 'Error'
