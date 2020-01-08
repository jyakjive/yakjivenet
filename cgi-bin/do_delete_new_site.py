#!D:/Python27/python.exe
##!/usr/bin/python

#imports

from shutil import *

import cgi
import cgitb; cgitb.enable()
import Cookie

import os

from db.tools import SiteDbCreator
from admin.site_handler import *
from admin.vars import *
from util.fileutils import dirExists
from newscommunity.ncvars import TRUE
from ui.sitemap import SitemapGenerator
from random import randint

siteDir = '../../cgi-bin/yj/'
htmlDir = '../../'

form = cgi.FieldStorage()

redirect = 'http://www.yakjive.net/cgi-bin/view_sites.py?rKey=' + str(randint(0,10000))
if ((not form.has_key('password')) or (form.getfirst('password') != 'jezebel22')):
    redirect = 'http://www.yakjive.com'
elif (form.has_key('domain')):

    # Extract the form values
    domain = form.getfirst('domain')
    permanent = form.getfirst('permanent')

    sites = loadSites(FILENAME_SITE_PROPERTIES)

    if (domain not in sites):
        raise Exception('Could not find site in Sites. ' + domain)

    if (sites[domain].status in [STATUS_GOOD, STATUS_INACTIVE]):
        # Simply disabled for safety's sake
        if (dirExists(sites[domain].rootAdminDir + domain)):
            rmtree(sites[domain].rootAdminDir + domain)
        if (dirExists(sites[domain].rootWWWDir + domain)):
            rmtree(sites[domain].rootWWWDir + domain)

        # Delete the database tables
        dbCreator = SiteDbCreator(sites[domain].id)
        dbCreator.cleanUp()

        # Terminate the site in the properties
        if (permanent in TRUE):
            del(sites[domain])
        else:
            sites[domain].status = STATUS_TERMINATED
        writeSites(FILENAME_SITE_PROPERTIES, sites)

        SitemapGenerator.writeSitemapArchiveXML(CREATE_WEBSITE_LOCATION)

print 'Location: ' + str(redirect)
print
