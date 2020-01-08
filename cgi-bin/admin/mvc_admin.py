# imports

import os
import cgi
import cgi
import time
from shutil import *

from admin_utils import *
from vars import *
from site_handler import *
from ui.mvc import *
from util.fileutils import *
from util.email import *
from classes.application_handler import *
from util.fileutils import *
from classes.newspage_utils import createBlankPage
from classes.newspage_handler import NewsPage
from db.tools import SiteDbCreator
from util.user_management import UserDataParser

# declarations

OP_CHECK_INVITE = 'check_invite'
OP_CREATE_SITE = 'create_site'
OP_ACTIVATE_SITE = 'activate_site'
OP_ERROR = 'error'

# classes

class AdminModel(Model):
    def __init__(self, form):
        Model.__init__(self, form)
        # Order is important!
        self.businessObjects = [
            AdminCheckInviteBO,
            AdminCreateSiteBO,
            AdminActivateSiteBO,
            AdminProcessErrorsBO]

        self.referer = INTERNAL_REFERER

    def getRouter(self, form = None):
        return AdminRouter(form, self)

    def validate(self):
        #raise str(repr(self.__dict__))
        check = 'operation' in self.__dict__

        if (check):
            if (self.operation == OP_CHECK_INVITE):
                check = check and ('inviteCode' in self.__dict__)
            elif (self.operation == OP_CREATE_SITE):

                check = check and ('inviteCode' in self.__dict__)
                check = check and ('domain' in self.__dict__)
                check = check and ('webmasterUsername' in self.__dict__)
                check = check and ('webmasterFirst' in self.__dict__)
                #check = check and ('webmasterLast' in self.__dict__)
                check = check and ('siteCategory' in self.__dict__)
                check = check and ('siteTitle' in self.__dict__)
                #check = check and ('siteSubTitle' in self.__dict__)
                #check = check and ('companyName' in self.__dict__)
                #check = check and ('metaKeywords' in self.__dict__)
                #check = check and ('metaDescription' in self.__dict__)
                check = check and ('webmasterEmail' in self.__dict__)
                check = check and ('webmasterPassword1' in self.__dict__)
                check = check and ('webmasterPassword2' in self.__dict__)
                check = check and ('webmasterNickname' in self.__dict__)

                if ('webmasterLast' not in self.__dict__):
                    self.webmasterLast = ''
                if ('siteSubTitle' not in self.__dict__):
                    self.siteSubTitle = ''
                if ('companyName' not in self.__dict__):
                    self.companyName = ''
                if ('metaKeywords' not in self.__dict__):
                    self.metaKeywords = ''
                if ('metaDescription' not in self.__dict__):
                    self.metaDescription = ''

                if (not check):
                    self.errorMessage = 'Failed create site validation'
            elif (self.operation == OP_ACTIVATE_SITE):
                check = check and ('activationCode' in self.__dict__)
                check = check and ('id' in self.__dict__)
                check = check and ('domain' in self.__dict__)
            else:
                check = False
        return check

class AdminRouter(FormRouter):
    def validate(self):
        check = FormRouter.validate(self)
        check = check and (self.model.operation != '')
        if (not check):
            self.model.errorMessage = 'Incorrect state to route page.'
        return check

    def getRoute(self):
        redir = DEFAULT_REDIRECT
        if (self.validate()):
            if (self.model.operation == OP_CHECK_INVITE):
                if (self.model.errorMessage == ''):
                    # if check invite has been successful, load the create page
                    redir = 'enter_site_info.py'
                else:
                    redir = 'bad_invite.py'
            elif (self.model.operation == OP_CREATE_SITE):
                if (self.model.errorMessage == ''):
                    # if create site has been successful, load the email notification page
                    redir = ROOT_SITE_MESSAGES_URL + 'site_created.html'
                else:
                    redir = 'enter_site_info.py'
            elif (self.model.operation == OP_ACTIVATE_SITE):
                if (self.model.errorMessage == ''):
                    # if activation has been successful, load the create page
                    redir = CUSTOM_SITE_ADMIN_URL + self.model.domain + '/login.py'
                    self.model.useForward = False
                else:
                    # if activation did not work
                    redir = ROOT_SITE_MESSAGES_URL + 'bad_activation.html'
            elif (self.model.operation == OP_ERROR):
                # if there has been an unexpected error
                redir = ROOT_SITE_MESSAGES_URL + 'error_on_creation.html'
        log('Redirecting to : ' + redir)
        return redir

class AdminCheckInviteBO(BusinessObject):
    ''' Check the invite code to make sure it's valid. '''
    def execute(self):
        if (self.model.operation == OP_CHECK_INVITE):
            if (self.model.inviteCode[0].find('YJBETAS') == 0):
                sites = loadSites(FILENAME_SITE_PROPERTIES)

                try:
                    code = int(self.model.inviteCode[len('YJBETAS'):])
                    check = False
                    for item in sites:
                        check = (item.id == code)
                        if (check):
                            break

                    if (not check):
                        self.model.errorMessage = 'Could not validate invite code [' + self.model.inviteCode + ']...'
                except:
                    self.model.errorMessage = 'Could not validate invite code [' + self.model.inviteCode + ']..'
            elif (self.model.inviteCode in INVITE_CODES):
                pass
            else:
                self.model.errorMessage = 'Could not validate invite code [' + self.model.inviteCode + '].'

class AdminCreateSiteBO(BusinessObject):
    def execute(self):
        if (self.model.operation == OP_CREATE_SITE):
            # load the sites
            sites = loadSites(FILENAME_SITE_PROPERTIES)

            lowerSiteNames = list()
            for item in sites:
                lowerSiteNames += [item.lower()]

            prefixesOk = True
            for item in SITE_NAMES_FORBIDDEN_PREFIXES:
                prefixesOk = prefixesOk and (self.model.domain.lower().find(item) != 0)

            if ((SITE_NAMES_MINIMUM_LENGTH > len(self.model.domain)) or
                    (self.model.domain.lower() in SITE_NAMES_FORBIDDEN) or
                    (not prefixesOk) or
                    (self.model.domain in lowerSiteNames)):
                self.model.errorMessage = 'The domain name \'' + self.model.domain + '\' is already in use or unavailable'
            elif (self.model.webmasterPassword1 != self.model.webmasterPassword2):
                self.model.errorMessage = 'The passwords you entered don\'t match'
            elif (self.model.webmasterPassword1 != self.model.webmasterPassword2):
                self.model.errorMessage = 'The password you entered is too short'
            elif (not checkAlphaNum(self.model.webmasterEmail, '@.')):
                self.model.errorMessage = 'The contact email was invalid'
            else:
                try:

                    # create a new site object and add it to sites
                    site = Site()
                    site.domain = self.model.domain
                    site.contactEmail = self.model.webmasterEmail
                    site.webmasterUsername = self.model.webmasterUsername
                    site.webmasterFirst = self.model.webmasterFirst
                    site.webmasterLast = self.model.webmasterLast
                    timestr = time.strftime('%Y-%m-%d', time.gmtime(time.time()))
                    site.dateCreated = timestr
                    site.activated = False
                    site.activationCode = getRandomKey(10)
                    site.inviteCode = self.model.inviteCode
                    site.rootAdminDir = CREATE_DEFAULT_LOCATION
                    site.rootWWWDir = CREATE_WEBSITE_LOCATION

                    sites[site.domain] = site

                    # create the new yj site    # Extract the form values
                    domain = self.model.domain
                    siteCategory = self.model.siteCategory
                    siteTitle = self.model.siteTitle
                    siteSubTitle = self.model.siteSubTitle
                    companyName = self.model.companyName
                    metaKeywords = self.model.metaKeywords
                    metaDescription = self.model.metaDescription
                    webmasterEmail = self.model.webmasterEmail
                    webmasterFirst = self.model.webmasterFirst
                    webmasterLast = self.model.webmasterLast
                    webmasterUsername = self.model.webmasterUsername
                    webmasterPassword = self.model.webmasterPassword1
                    webmasterKey = getRandomKey(10)
                    webmasterNickname = self.model.webmasterNickname
                    rootURL = CREATE_ROOT_URL

                    # Replace keys in the right files
                    replaceDict = {
                        'domain': domain,
                        'ID': site.id,
                        'siteCategory': siteCategory,
                        'siteTitle': siteTitle,
                        'siteSubTitle': siteSubTitle,
                        'companyName': companyName,
                        'metaKeywords': metaKeywords,
                        'metaDescription': metaDescription,
                        'webmasterEmail': webmasterEmail,
                        'webmasterFirst': webmasterFirst,
                        'webmasterLast': webmasterLast,
                        'webmasterUsername': webmasterUsername,
                        'webmasterPassword': webmasterPassword,
                        'webmasterKey': webmasterKey,
                        'webmasterNickname': webmasterNickname,
                        'webmasterNicknameFiltered': webmasterNickname.replace(' ', '-'),
                        'rootURL': CREATE_ROOT_URL,
                        'siteURL': CREATE_ROOT_URL + '/' + domain + '/'}

                    log('About to copy from site_template to ' + CREATE_DEFAULT_LOCATION + domain)
                    copytree('site_template', CREATE_DEFAULT_LOCATION + domain)
                    log('About to copy from site_template_html to ' + CREATE_WEBSITE_LOCATION + domain)
                    copytree('site_template_html', CREATE_WEBSITE_LOCATION + domain)
                    log('Finished copy')

                    # Replace the keys in the prop files
                    for item in CREATE_REPLACE_FILES:
                        filename = item
                        filename = filename.replace('${domain}', domain)
                        data = readTextFile(filename, replaceDict = replaceDict)
                        writeTextFile(filename, data)

                    # CHMOD all the right py files
                    files = os.listdir(CREATE_DEFAULT_LOCATION + domain)
                    for f in files:
                        if (f[len(f) - 3:len(f)].upper() == '.PY'):
                            os.chmod(CREATE_DEFAULT_LOCATION + domain + '/' + f, 0711)
                    os.chmod(CREATE_DEFAULT_LOCATION + domain + '/cgiemail', 0711)

                    # Copy the blog template to it's right name
                    #for item in CREATE_COPY_FILES:
                    #    file1 = item.replace('${domain}', domain)
                    #    file2 = CREATE_COPY_FILES[item].replace('${domain}', domain).replace('${webmasterTemplate}', webmasterNickname.replace(' ', '-'))
                    #    os.rename(file1, file2)

                    # Create the database tables
                    dbCreator = SiteDbCreator(site.id)
                    try:
                        dbCreator.cleanUp() # Do this in case there was a failure
                    except:
                        pass
                    dbCreator.execute()

                    newsPage = NewsPage(name=UserDataParser.getBlogPageName(webmasterNickname))
                    createBlankPage(newsPage, site.id)

                    # email the webmaster with instructions
                    replaceDict = dict()
                    replaceDict['domain'] = domain
                    replaceDict['fromEmail'] = EMAIL_INFO
                    replaceDict['toEmail'] = webmasterEmail
                    replaceDict['problemEmail'] = EMAIL_PROBLEM
                    replaceDict['subject'] = 'Welcome to YakJive'
                    replaceDict['toName'] = webmasterFirst
                    replaceDict['rootURL'] = ROOT_SITE_URL
                    replaceDict['adminURL'] = CUSTOM_SITE_ADMIN_URL
                    replaceDict['username'] = webmasterUsername
                    replaceDict['password'] = webmasterPassword
                    replaceDict['penname'] = webmasterNickname
                    replaceDict['code'] = 'S' + str(site.id) + 'B'
                    replaceDict['activationURL'] = ROOT_SITE_ADMIN_URL + 'dispatch_site_creation.py?' + \
                        'id=' + str(site.id) + '&' + \
                        'domain=' + str(site.domain) + '&' + \
                        'activationCode=' + str(site.activationCode) + '&' + \
                        'operation=' + OP_ACTIVATE_SITE

                    emailBody = readTextFile(EMAIL_INCLUDE_DIR + FILENAME_EMAIL_WELCOME, True, replaceDict)

                    log('About to send mail from ' + EMAIL_INFO + ' to ' + webmasterEmail + ' contents:\n\t' + emailBody[0:100])
                    sendEmail(EMAIL_INFO, webmasterEmail, emailBody)

                    # write the sites out to a file
                    writeSites(FILENAME_SITE_PROPERTIES, sites)
                except Exception, e:

                    deleteOk = True
                    try:
                        # Delete just created site
                        rmtree(CREATE_DEFAULT_LOCATION + domain)
                        rmtree(CREATE_WEBSITE_LOCATION + domain)
                    except:
                        deleteOk = False

                    self.model.errorMessage = 'Exception in AdminCreateSiteBO\n<br>' + repr(type(e)) + '\n<br>' + repr(e.args)
                    if (not deleteOk):
                        log('AdminCreateSiteBO: delete not ok: ' + self.model.errorMessage)
                        self.model.errorMessage += '\n<br>Unable to clean up'
                        self.model.operation = OP_ERROR
                    else:
                        log('AdminCreateSiteBO: delete ok: ' + self.model.errorMessage)
                        self.model.errorMessage = 'The system was unable to process the information given.  Please ' + \
                            'verify the email addresses that you entered and try again.'

class AdminActivateSiteBO(BusinessObject):
    def execute(self):
        try:
            if (self.model.operation == OP_ACTIVATE_SITE):
                log('About to activate site ' + self.model.domain)
                # load sites and find the site using the domain, id, and activation code
                sites = loadSites(FILENAME_SITE_PROPERTIES)
                site = sites[self.model.domain]
                if (site is None):
                    log('Domain doesn\'t exist ' + self.model.domain)
                    self.model.errorMessage = '1' # domain doesn't exist
                elif ((site.id != int(self.model.id))
                        or (site.domain != self.model.domain)
                        or (site.activationCode != self.model.activationCode)):
                    log('Couldn\'t authenticate ' + self.model.domain + ' ' + self.model.id + ' ' + self.model.activationCode \
                         + ' ' + site.domain + ' ' + str(site.id) + ' ' + site.activationCode)
                    self.model.errorMessage = '2' # couldn't authenticate
                elif (site.activated):
                    log('Site already activated ' + self.model.domain)
                    self.model.errorMessage = '3' # site already activated
                else:
                    log('Found site ' + self.model.domain)
                    # load the app_properties.xml for the particular site
                    filename = CREATE_DEFAULT_LOCATION + self.model.domain + '/data/app_properties.xml'
                    siteProps = loadApplication(filename)

                    # change the app_properties to activate the site (active = True)
                    siteProps.active = True

                    # write out the app properties for the site
                    siteAppProps = writeApplication(filename, siteProps)

                    # change the current site object to be activated (activated = True)
                    site.activated = True
                    writeSites(FILENAME_SITE_PROPERTIES, sites)
        except Exception, e:
            self.model.errorMessage = 'Exception in AdminActivateSiteBO\n<br>' + repr(type(e)) + '\n<br>' + repr(e.args)
            log(self.model.errorMessage)
            self.model.operation = OP_ERROR

class AdminProcessErrorsBO(BusinessObject):
    def execute(self):
        if (self.model.operation == OP_ERROR):
            emailDict = dict()
            emailDict['error'] = self.model.errorMessage
            emailDict['domain'] = 'site creation'
            emailDict['fromEmail'] = EMAIL_PROBLEM
            emailDict['toEmail'] = EMAIL_PROBLEM
            emailDict['subject'] = 'YakJive Exception -- Site Creation -- ' + self.model.errorMessage[0:20]

            emailBody = readTextFile(FILENAME_EMAIL_PROBLEM, True, emailDict)

            sendEmail(EMAIL_PROBLEM, EMAIL_PROBLEM, emailBody)