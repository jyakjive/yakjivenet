#!D:/Python27/python.exe
##!/usr/bin/python

#imports

from shutil import *

import cgi
import cgitb; cgitb.enable()
import Cookie

import os

from admin.site_handler import *
from admin.vars import *
from newscommunity.ncvars import TRUE
from time import strptime

sites = loadSites(FILENAME_SITE_PROPERTIES)

siteList = list()

for site in sites:
    siteList += [sites[site]]

if (len(siteList) > 2):
    for i in range(0, len(siteList) - 1):
        for j in range(i, len(siteList)):
            try:
                if (strptime(siteList[i].dateCreated, SITE_TIME_FORMAT) <
                        strptime(siteList[j].dateCreated, SITE_TIME_FORMAT)):
                   ii = siteList[i]
                   siteList[i] = siteList[j]
                   siteList[j] = ii
            except:
                   pass

body = ''

for site in siteList:
    delTxt = '<a href="delete_new_site.py?domain=' + site.domain + '">X</a>'
    body += ('<tr>\n<td>%s</td>\n<td><a href="http://www.yakjive.com/%s">%s</a></td>\n<td>%s</td>\n<td>%s</td>\n<td>%s</td>\n<td>%s</td>\n<td>%s</td>\n<td>%s</td>\n</tr>' %
        (site.id, site.domain, site.domain, site.webmasterFirst, site.webmasterLast, site.contactEmail, site.activated, site.dateCreated, delTxt))

body = ('<table>\n<th>ID</th>\n<th>Domain</th>\n<th>First</th>\n<th>Last</th>\n<th>Email</th>\n<th>Activated</th>\n<th>Date</th>\n<th>Del</th>\n%s</table>' %
    (body))
body = ('''
<html>
<head>
<title>YJ.NET View Sites</title>
</head>
<body>
<h1>All sites</h1>
%s
</body
</html>
''' % (body))

print "Content-Type: text/html\n"     # HTML is following
print body
