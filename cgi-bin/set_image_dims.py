#!D:/Python27/python.exe
##!/usr/bin/python

# Copies the sandbox to the template dir, then the template dir out to the site instances

#imports
#import util.properties
#import util.exceptions
#import util.user_management
from shutil import *
from stat import *

import cgi
import cgitb; cgitb.enable()
import Cookie

import os

from util.fileutils import *
from util.image_utils import *
from admin.site_handler import *
from admin.vars import *

from classes.application_handler import *

from db.attachment_dao import *

# Definitons

# Declarations
sites = loadSites(FILENAME_SITE_PROPERTIES)

cookie = Cookie.SimpleCookie()
form = cgi.FieldStorage()

redirect = 'http://www.yakjive.net'
if ((not form.has_key('password')) or (form.getfirst('password') != 'jezebel22')):
    redirect += '?error=npwd'
else:
    hasError = False

    for domain in sites:
        adao = AttachmentDaoFactory.create(sites[domain].id);
        try:
            aList = adao.fetch()
            for attach in aList:
                if (attach.image):
                    try:
                        apfilename = CREATE_DEFAULT_LOCATION + domain + '/data/app_properties.xml'
                        siteProps = loadApplication(apfilename)
                        attachDir = siteProps.absoluteRootPath + siteProps.attachDirectory.replace('../', '')
                        ii = ImageInfo(attachDir + attach.filename)
                        attach.imageHeight = ii.height
                        attach.imageWidth = ii.width
                        adao.write(None, attach)
                    except IOError, e:
                        log(str(e))
        finally:
            adao.cleanUp();

print 'Location: ' + str(redirect)
#print cookie
print
