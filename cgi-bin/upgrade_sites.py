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
from admin.site_handler import *
from admin.vars import *

from db.tools import SiteDbCreator

# Definitons
def doReplace(data, replaceDict):
    for item in replaceDict:
        data = data.replace('${' + item + '}', replaceDict[item])
    return data

# Declarations
header = ''
body = ''
footer = ''

# siteDir = '../../cgi-bin/yj/'

sandbox = 'testsite'
template = 'site_template'

rootLocation = '..'
sandboxHtml = '../testsite'
templateHtml = 'site_template_html'
includeDir = 'data/page_includes'
sqlDir = 'data/sql/'

scripts = 'scripts'
support = 'supportfiles'
styles = 'styles'


packageDirs = [
    'admin',
    'classes',
    'newscommunity',
    'util',
    'ui',
    'db'
    ]


def copyFiles(src, dst, ext, mod = 0):
    ext = ext.upper()
    origfiles = os.listdir(src)
    for f in origfiles:
        if (f[0:5] != 'test_'): # Skip test scripts
            if (f[len(f) - len(ext):len(f)].upper() == ext):
                copy(src + '/' + f, dst+ '/' + f)
                if (mod > 0):
                    os.chmod(dst + '/' + f, mod)

def execCopy(src, srcHtml, dst, dstHtml, rootDir = None):

    # Include files of HTML and TXT type
    copyFiles(src + '/' + includeDir, dst + '/' + includeDir, '.HTML')
    copyFiles(src + '/' + includeDir, dst + '/' + includeDir, '.TXT')

    # Root Python files
    copyFiles(src, dst, '.PY', 0711)

    # Python packages
    for d in packageDirs:
        if (not dirExists(dst + '/' + d)):
            os.mkdir(dst + '/' + d, 0711)
        copyFiles(src + '/' + d, dst + '/' + d, '.PY')

    # CSS Files
    copyFiles(srcHtml, dstHtml, '.CSS')

    # TXT Files -- not sure this is still necessary
    copyFiles(srcHtml + '/' + support, dstHtml + '/' + support, '.TXT')

    # Copy the styles and scripts dirs to yakjive.com and all sites that use their own domain
    # This does NOT get executed for every site
    if (rootDir is not None):
        srcScriptDir = rootDir + '/' + scripts
        dstScriptDir = dstHtml + '/' + scripts
        if (dirExists(dstScriptDir)):
            rmtree(dstScriptDir)
        # JS Files
        copytree(srcScriptDir, dstScriptDir)

        srcStylesDir = rootDir + '/' + styles
        dstStylesDir = dstHtml + '/' + styles
        if (dirExists(dstStylesDir)):
            rmtree(dstStylesDir)
        # style Files
        copytree(srcStylesDir, dstStylesDir)
    else:
        # clean up old stuff, if it's there
        if (dirExists(dstHtml + '/' + scripts)):
            rmtree(dstHtml + '/' + scripts)
        if (dirExists(dstHtml + '/' + styles)):
            rmtree(dstHtml + '/' + styles)

sites = loadSites(FILENAME_SITE_PROPERTIES)

cookie = Cookie.SimpleCookie()
form = cgi.FieldStorage()

redirect = 'https://www.yakjive.net'
if ((not form.has_key('password')) or (form.getfirst('password') != 'jezebel22')):
    redirect += '?error=npwd'
else:
    hasError = False

    # SQL updates
    dirFound = True
    dirIndex = 2 # The first upgrade is version 2
    dirFound = dirExists(sqlDir + 'v' + str(dirIndex))
    while(dirFound):
        dirFound = dirExists(sqlDir + 'v' + str(dirIndex + 1))
        if (dirFound):
            dirIndex += 1

    for domain in sites:
        updatedSqlVersion = 0
        if (sites[domain].sqlVersion < dirIndex):
            log(str(range(sites[domain].sqlVersion + 1, dirIndex + 1)))
            for v in range(sites[domain].sqlVersion + 1, dirIndex + 1):
                upgradeDir = sqlDir + 'v' + str(v) + '/'
                log('About to call site creator for site ' + domain + '(' + str(sites[domain].id) + ') and directory ' + upgradeDir)
                sdc = SiteDbCreator(sites[domain].id)
                sdc.upgrade(upgradeDir, sites[domain].id)
                updatedSqlVersion = v
        if (updatedSqlVersion > sites[domain].sqlVersion):
            sites[domain].sqlVersion = updatedSqlVersion
            writeSites(FILENAME_SITE_PROPERTIES, sites)

    # Copy the sandbox to the template dir
    execCopy(sandbox, sandboxHtml, template, templateHtml)

    # Upgrade the individual sites from the template
    for domain in sites:
        try:
            if (sites[domain].status in [STATUS_GOOD, STATUS_INACTIVE]):
                log('About to upgrade: ' + sites[domain].rootAdminDir + '  ' + domain)
                #mode = os.stat(sites[domain].rootAdminDir)[ST_MODE]
                #if S_ISDIR(mode):
                if (domain == 'yakjive'):
                    execCopy(template, templateHtml, sites[domain].rootAdminDir, sites[domain].rootWWWDir, rootDir = rootLocation)
                else:
                    if (('/' + domain + '/') not in sites[domain].rootAdminDir):
                        # a child site of yakjive.com
                        execCopy(template, templateHtml, sites[domain].rootAdminDir + domain, sites[domain].rootWWWDir + domain)
                    else:
                        # a site that uses it's own domain
                        execCopy(template, templateHtml, sites[domain].rootAdminDir, sites[domain].rootWWWDir + domain, rootDir = rootLocation)
        except Exception, e:
            log('Error attempting to upgrade site (' + domain + '): ' + str(e))
print 'Location: ' + str(redirect)
#print cookie
print
