
# imports

from newscommunity.application import APPLICATION
from newscommunity.ncvars import *
from util.fileutils import readTextFile
from util.html_utils import *
import cgi

import os

# definitions

def getStandardReplaceDict():
    replaceDict = dict()
    replaceDict['rootURL'] = APPLICATION.rootURL
    replaceDict['domain'] = APPLICATION.domainName
    replaceDict['siteTitle'] = APPLICATION.siteTitle
    replaceDict['styleURL'] = APPLICATION.styleURL
    replaceDict['siteID'] = APPLICATION.siteID
    replaceDict['metaKeywords'] = APPLICATION.metaKeywords
    replaceDict['metaDescription'] = APPLICATION.metaDescription
    replaceDict['miloSays'] = miloSayingGenerator()
    replaceDict['hideStart'] = ''
    replaceDict['hideEnd'] = ''
    return replaceDict

def printConsolePage(body, replaceDict = None, cookie = None):
    newdict = getStandardReplaceDict()
    if (replaceDict is not None):
        for item in replaceDict:
            newdict[item] = replaceDict[item]
    printPage(APPLICATION.headerFile, body, APPLICATION.footerFile, newdict, cookie)

    # FOR INFO PURPOSES ONLY.  NOT FOR PRODUCTION.
    #f or item in os.environ:
    #    print item + ': ' + os.environ[item] + '<br>\n'
    #f 2 = cgi.FieldStorage()
    #p rint
    #p rint 'HEADERS'
    #f or item in f2.headers:
    #    print item + ': ' + f2.headers[item] + '<br>'
    #p rint
    #p rint 'FORM KEYS'
    #f or item in f2.keys():
    #    print item + ': ' + f2.getfirst(item) + '<br>'

def getPopupHTML(body, replaceDict = None):
    ''' Load a template file for the popup window and populate it. '''
    #Load the header file
    if (replaceDict is not None):
        srd = getStandardReplaceDict()
        for item in srd:
            if (item not in replaceDict):
                replaceDict[item] = srd[item]
    else:
        replaceDict = getStandardReplaceDict()
    page = readTextFile(FILENAME_POPUP_TEMPLATE, replaceDict)
    page = page.replace('${body}', body)
    return page
