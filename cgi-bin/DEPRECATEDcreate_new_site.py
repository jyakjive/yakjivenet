#!/usr/bin/python
##!C:/apps/python24/python.exe

#imports
#import util.properties
#import util.exceptions
#import util.user_management
from shutil import *

import cgi
import cgitb; cgitb.enable()
import Cookie

import os

from util.fileutils import *

# Definitons
def doReplace(data, replaceDict):
    for item in replaceDict:
        data = data.replace('${' + item + '}', replaceDict[item])
    return data

# Declarations
header = ''
body = ''
footer = ''

siteDir = 'yj/'

replaceFiles = [ \
    siteDir + '${domain}/data/app_properties.xml', \
    siteDir + '${domain}/data/page_properties.xml', \
    siteDir + '${domain}/data/rss2_properties.xml', \
    siteDir + '${domain}/data/section_properties.xml', \
    siteDir + '${domain}/data/user_properties.xml', \
    siteDir + '${domain}/data/user_roles.xml', \
    siteDir + '${domain}/data/newsItems/template-blog-data.xml', \
    '../${domain}/admin/index.html']

copyFiles = { \
    siteDir + '${domain}/data/newsItems/template-blog-data.xml': \
    siteDir + '${domain}/data/newsItems/${webmasterTemplate}-blog-data.xml'}

cookie = Cookie.SimpleCookie()

#appParser = util.properties.PropertyDataParser(FILENAME_APPLICATION)
#util.exceptions.handleExceptions(appParser.getProperties())

#userParser = util.user_management.UserDataParser(FILENAME_USERS)

#cookieName = str(appParser.getProperty('cookieName'))
#redirect = str(appParser.getProperty('redirectOnFailedLogin'))


form = cgi.FieldStorage()

redirect = 'http://www.yakjive.com'
if ((not form.has_key('password')) or (form.getfirst('password') != 'jezebel22')):
    redirect = 'http://www.yakjive.com'
elif (form.has_key('domain')):

    # Extract the form values
    domain = form.getfirst('domain')
    siteCategory = form.getfirst('siteCategory')
    siteTitle = form.getfirst('siteTitle')
    siteSubTitle = form.getfirst('siteSubTitle')
    companyName = form.getfirst('companyName')
    metaKeywords = form.getfirst('metaKeywords')
    metaDescription = form.getfirst('metaDescription')
    webmasterEmail = form.getfirst('webmasterEmail')
    webmasterFirst = form.getfirst('webmasterFirst')
    webmasterLast = form.getfirst('webmasterLast')
    webmasterUsername = form.getfirst('webmasterUsername')
    webmasterPassword = form.getfirst('webmasterPassword')
    webmasterKey = form.getfirst('webmasterKey')
    webmasterNickname = form.getfirst('webmasterNickname')
    rootURL = form.getfirst('rootURL')

    # Set the redirect location # TODO: Fix this
    redirect = 'http://' + rootURL + '/cgi-bin/' + siteDir + domain + '/login.py'

    # Replace keys in the right files
    replaceDict = { \
        'domain': domain,\
        'siteCategory': siteCategory, \
        'siteTitle': siteTitle, \
        'siteSubTitle': siteSubTitle, \
        'companyName': companyName, \
        'metaKeywords': metaKeywords, \
        'metaDescription': metaDescription, \
        'webmasterEmail': webmasterEmail, \
        'webmasterFirst': webmasterFirst, \
        'webmasterLast': webmasterLast, \
        'webmasterUsername': webmasterUsername, \
        'webmasterPassword': webmasterPassword, \
        'webmasterKey': webmasterKey, \
        'webmasterNickname': webmasterNickname, \
        'rootURL': rootURL, \
        'siteURL': rootURL + '/' + domain + '/'}

    # Simply disabled for safety's sake
    copytree('site_template', siteDir + domain)
    copytree('site_template_html', '../' + domain)

    # Replace the keys in the prop files
    for item in replaceFiles:
        filename = item
        filename = filename.replace('${domain}', domain)
        data = loadTextFile(filename)

        data = doReplace(data, replaceDict)

        writeTextFile(filename, data)

   # CHMOD all the right py files
    files = os.listdir(siteDir + domain)
    for f in files:
        if (f[len(f) - 3:len(f)].upper() == '.PY'):
            os.chmod(siteDir +domain + '/' + f, 0711)
    os.chmod(siteDir +domain + '/cgiemail', 0711)

    # Copy the blog template to it's right name
    for item in copyFiles:
        file1 = item.replace('${domain}', domain)
        file2 = copyFiles[item].replace('${domain}', domain).replace('${webmasterTemplate}', webmasterNickname)
        os.rename(file1, file2)

#if (form.has_key('username') & form.has_key('password')):
#    key = userParser.login(form.getfirst('username'),form.getfirst('password'))
#    if (key <> None):
#        redirect = appParser.getProperty('startPage')
#        cookie[cookieName] = key

print 'Location: ' + str(redirect)
#print cookie
print
