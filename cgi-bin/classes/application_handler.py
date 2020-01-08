'''Classes to load and store the application properties.'''
# Imports
from util.properties import *
from util.fileutils import Semaphore
from newscommunity.ncvars import *

# Declarations
semname = 'application'

# Definitions

def loadApplication(filename):
    '''Create a new dictionary of news sections by passing
    in a file name to the section properties file.'''

    sem = Semaphore(semname)
    sem.put()

    parser = PropertyDataParser(filename)

    sem.remove()

    application = Application()

    application.siteTitle = parser.getSafeProperty('siteTitle', '')
    application.siteSubTitle = parser.getSafeProperty('siteSubTitle', '')
    application.metaDescription = parser.getSafeProperty('metaDescription', '')
    application.metaKeywords = parser.getSafeProperty('metaKeywords', '')
    application.category = parser.getSafeProperty('category', '')

    application.cookieName = parser.getSafeProperty('cookieName', '')
    application.rootURL = parser.getSafeProperty('rootURL', '')
    application.siteID = parser.getSafeProperty('siteID', '')
    application.ID = parser.getSafeProperty('ID', '')
    application.dataDirectory = parser.getSafeProperty('dataDirectory', '')
    application.includesDirectory = parser.getSafeProperty('includesDirectory', '')
    application.rssDirectory = parser.getSafeProperty('rssDirectory', '')
    application.rssFullURL = parser.getSafeProperty('rssFullURL', '')
    application.newsFileLocation = parser.getSafeProperty('newsFileLocation', '')
    application.exceptionHeader = parser.getSafeProperty('exceptionHeader', '')
    application.exceptionFooter = parser.getSafeProperty('exceptionFooter', '')
    application.headerFile = parser.getSafeProperty('headerFile', '')
    application.footerFile = parser.getSafeProperty('footerFile', '')

    application.redirectOnFailedLogin = parser.getSafeProperty('redirectOnFailedLogin', '')
    application.startPage = parser.getSafeProperty('startPage', '')
    application.homePage = parser.getSafeProperty('homePage', '')

    application.templateDir = parser.getSafeProperty('templateDir', '')
    application.indexTemplate = parser.getSafeProperty('indexTemplate', '')

    application.domainName = parser.getSafeProperty('domainName', '')
    application.adminCssFile = parser.getSafeProperty('adminCssFile', '')
    application.attachDirectory = parser.getSafeProperty('attachDirectory', '')
    application.attachURL = parser.getSafeProperty('attachURL', '')
    application.userDirectory = parser.getSafeProperty('userDirectory', '')
    application.userURL = parser.getSafeProperty('userURL', '')
    application.active = (parser.getSafeProperty('active', True) in TRUE)
    application.premium = (parser.getSafeProperty('premium', False) in TRUE)
    application.showAds = (parser.getSafeProperty('showAds', True) in TRUE)
    application.storageLocked = (parser.getSafeProperty('storageLocked', False) in TRUE)
    application.siteType = parser.getSafeProperty('siteType', SITE_TYPE_BASIC)
    application.newsletter = (parser.getSafeProperty('newsletter', True) in TRUE)

    application.styleURL = parser.getSafeProperty('styleURL', '')
    application.printStyleURL = parser.getSafeProperty('printStyleURL', application.styleURL)
    application.styleDir = parser.getSafeProperty('styleDir', '')
    application.styleName = parser.getSafeProperty('styleName', '')
    application.customStyle = (parser.getSafeProperty('customStyle', False) in TRUE)

    application.subTitleDate = (parser.getSafeProperty('subTitleDate', False) in TRUE)
    application.articleDate = (parser.getSafeProperty('articleDate', True) in TRUE)
    application.moreText = parser.getSafeProperty('moreText', '[more]')
    application.imageSize = int(parser.getSafeProperty('imageSize', 60))
    application.advancedLinks = (parser.getSafeProperty('advancedLinks', False) in TRUE)

    application.adminURL = parser.getSafeProperty('adminURL', '')
    application.contactEmail = parser.getSafeProperty('contactEmail', '')

    application.autoResizeImages = (parser.getSafeProperty('autoResizeImages', True) in TRUE)
    application.maxImageSize = int(parser.getSafeProperty('maxImageSize', 250000))
    application.absoluteRootPath = parser.getSafeProperty('absoluteRootPath', '/home/yakjivec/www/')
    application.allowRTEToggleSrc = (parser.getSafeProperty('allowRTEToggleSrc', False) in TRUE)

    application.db = parser.getSafeProperty('db', '')
    application.dbUser = parser.getSafeProperty('dbUser', '')
    application.dbPassword = parser.getSafeProperty('dbPassword', '')

    return application

def writeApplication(filename, application):
    '''Write the sections properties file.'''

    pfb = PropertyFileBuilder()
    pfb.setCData(True)

    propDict = application.getPropDict()

    for prop in propDict:
        pfb.add(prop, propDict[prop])

    sem = Semaphore(semname)
    sem.put()

    pfb.write(filename)

    sem.remove()

# Classes
class Application:
    def __init__(self):
        self.cookieName = ''
        self.siteID = ''
        self.ID = ''
        self.rootURL = ''
        self.dataDirectory = ''
        self.includesDirectory = ''
        self.rssDirectory = ''
        self.rssFullURL = ''
        self.newsFileLocation = ''
        self.exceptionHeader = ''
        self.exceptionFooter = ''
        self.headerFile = ''
        self.footerFile = ''

        self.redirectOnFailedLogin = ''
        self.startPage = ''
        self.homePage = ''

        self.templateDir = ''
        self.indexTemplate = ''

        self.domainName = ''
        self.adminCssFile = ''
        self.attachDirectory = ''
        self.attachURL = ''
        self.userDirectory = ''
        self.userURL = ''
        self.active = True
        self.premium = False
        self.siteType = SITE_TYPE_BASIC
        self.showAds = True
        self.storageLocked = False
        self.newsletter = True

        self.siteTitle = ''
        self.siteSubTitle = ''
        self.metaKeywords = ''
        self.metaDescription = ''
        self.category = ''

        self.styleURL = ''
        self.printStyleURL = ''
        self.styleDir = ''
        self.customStyle = False
        self.styleName = ''

        self.subTitleDate = False
        self.articleDate = False
        self.moreText = '[more]'
        self.imageSize = 60 # Size of thumbnail dimension

        self.adminURL = ''
        self.contactEmail = ''
        self.advancedLinks = False

        self.autoResizeImages = True
        self.maxImageSize = 250000 # max file size

        self.visProperties = dict()
        self.propDict = dict()

        self.absoluteRootPath = ''
        self.allowRTEToggleSrc = False

        # TODO: Consider encrypting these or putting them someplace else
        self.db = ''
        self.dbUser = ''
        self.dbPassword = ''

    def getEditableProperties(self):
        '''Return a list of editable properties.'''
        data = list()

        data += ['contactEmail']
        #data += ['adBannerPosition']
        data += ['newsletter']
        data += ['siteTitle']
        data += ['siteSubTitle']
        data += ['metaDescription']
        data += ['metaKeywords']
        data += ['subTitleDate']
        data += ['articleDate']
        data += ['moreText']
        data += ['imageSize']
        data += ['menuSeparator']
        data += ['advancedLinks']
        data += ['autoResizeImages']
        data += ['maxImageSize']
        data += ['allowRTEToggleSrc']

        return data

    def getVisibleProperties(self):
        '''Return a dictionary of displayable properties and their
        pretty name.'''

        if (len(self.visProperties) == 0):
            # Put these in the order in which they
            # should appear on the properties GUI
            self.visProperties['siteTitle'] = 'Site title'
            self.visProperties['siteSubTitle'] = 'Site subtitle'
            self.visProperties['metaDescription'] = 'Description'
            self.visProperties['metaKeywords'] = 'Keywords'
            #self.visProperties['category'] = 'Category'
            self.visProperties['rootURL'] = 'Site root URL'
            self.visProperties['rootURL'] = 'Home page URL'
            self.visProperties['domainName'] = 'Domain name'
            self.visProperties['contactEmail'] = 'Contact email'
            self.visProperties['active'] = 'Site is active'
            self.visProperties['siteType'] = 'Site type'
            self.visProperties['showAds'] = 'Show ads'
            self.visProperties['newsletter'] = 'Use newsletter'
            self.visProperties['styleName'] = 'Site style'
            self.visProperties['siteID'] = 'Site ID'
            self.visProperties['subTitleDate'] = 'Add date to page subtitles'
            self.visProperties['articleDate'] = 'Add dates to articles'
            self.visProperties['moreText'] = 'Link text for \'more\' article info'
            self.visProperties['imageSize'] = 'Thumbnail image size'
            self.visProperties['autoResizeImages'] = 'Automatically resize images'
            self.visProperties['allowRTEToggleSrc'] = 'Allow users to show the HTML when editing articles'
            #self.visProperties['maxImageSize'] = 'Maximum image size (bytes)'
            #self.visProperties['rssFullURL'] = 'RSS base URL'
            #self.visProperties['adminCssFile'] = 'Admin CSS file'
            #self.visProperties['storageLocked'] = 'Over storage limit'
            #self.visProperties['advancedLinks'] = 'Use advanced autolinks'
        return self.visProperties

    def getPropDict(self):
        if (len(self.propDict) == 0):
            # Put these in the order in which they
            # should appear on the properties GUI
            self.propDict['ID'] = self.ID
            self.propDict['siteID'] = self.siteID
            self.propDict['siteTitle'] = self.siteTitle
            self.propDict['siteSubTitle'] = self.siteSubTitle
            self.propDict['metaDescription'] = self.metaDescription
            self.propDict['metaKeywords'] = self.metaKeywords
            self.propDict['category'] = self.category
            self.propDict['adminURL'] = self.adminURL
            self.propDict['contactEmail'] = self.contactEmail

            self.propDict['cookieName'] = self.cookieName
            self.propDict['rootURL'] = self.rootURL
            self.propDict['dataDirectory'] = self.dataDirectory
            self.propDict['includesDirectory'] = self.includesDirectory
            self.propDict['rssDirectory'] = self.rssDirectory
            self.propDict['rssFullURL'] = self.rssFullURL
            self.propDict['newsFileLocation'] = self.newsFileLocation
            self.propDict['exceptionHeader'] = self.exceptionHeader
            self.propDict['exceptionFooter'] = self.exceptionFooter
            self.propDict['headerFile'] = self.headerFile
            self.propDict['footerFile'] = self.footerFile
            self.propDict['redirectOnFailedLogin'] = self.redirectOnFailedLogin
            self.propDict['startPage'] = self.startPage
            self.propDict['homePage'] = self.homePage
            self.propDict['templateDir'] = self.templateDir
            self.propDict['indexTemplate'] = self.indexTemplate
            self.propDict['domainName'] = self.domainName
            self.propDict['adminCssFile'] = self.adminCssFile
            self.propDict['attachDirectory'] = self.attachDirectory
            self.propDict['attachURL'] = self.attachURL
            self.propDict['userDirectory'] = self.userDirectory
            self.propDict['userURL'] = self.userURL
            self.propDict['active'] = self.active
            self.propDict['premium'] = self.premium
            self.propDict['storageLocked'] = self.storageLocked
            self.propDict['siteType'] = self.siteType
            self.propDict['showAds'] = self.showAds
            self.propDict['newsletter'] = self.newsletter

            self.propDict['styleURL'] = self.styleURL
            self.propDict['printStyleURL'] = self.printStyleURL
            self.propDict['styleDir'] = self.styleDir
            self.propDict['customStyle'] = self.customStyle
            self.propDict['styleName'] = self.styleName

            self.propDict['subTitleDate'] = self.subTitleDate
            self.propDict['articleDate'] = self.articleDate
            self.propDict['moreText'] = self.moreText
            self.propDict['imageSize'] = self.imageSize
            self.propDict['advancedLinks'] = self.advancedLinks

            self.propDict['autoResizeImages'] = self.autoResizeImages
            self.propDict['maxImageSize'] = self.maxImageSize
            self.propDict['absoluteRootPath'] = self.absoluteRootPath
            self.propDict['allowRTEToggleSrc'] = self.allowRTEToggleSrc

            self.propDict['db'] = self.db
            self.propDict['dbUser'] = self.dbUser
            self.propDict['dbPassword'] = self.dbPassword
        return self.propDict
