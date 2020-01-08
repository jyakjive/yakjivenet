

#Imports
import xml.parsers.expat
from random import randint
from util.properties import *
from util.fileutils import Semaphore, readTextFile
from newscommunity.ncvars import *
from classes.article import Attachment
from newscommunity.application import APPLICATION
from email import sendEmail
from string import join

#parser declarations

# Indicate that a particular part of a rule has no following rule indicators
UR_HAS_CHILDREN = True
# Indicate that a particular part of a rule has following rule indicators
UR_NO_CHILDREN = False

UR_USERS = 'users'
UR_PAGES = 'pages'
UR_SECTIONS = 'sections'
UR_USERRULES = 'userrules'
UR_ARTICLES = 'articles'
UR_NEWSLETTER = 'newsletter'

UR_APPLICATIONS = {\
    UR_USERS:['Users', UR_HAS_CHILDREN], \
    UR_PAGES:['Pages', UR_HAS_CHILDREN], \
    UR_USERRULES:['User Rules', UR_NO_CHILDREN], \
    UR_ARTICLES:['Articles', UR_HAS_CHILDREN], \
    UR_SECTIONS:['Sections', UR_NO_CHILDREN], \
    UR_NEWSLETTER:['Newsletter subscriptions', UR_NO_CHILDREN]}

UR_APPLICATIONS_PRETTY = dict()
uakeys = UR_APPLICATIONS.keys()
uakeys.sort()
for item in uakeys:
    UR_APPLICATIONS_PRETTY[item] = UR_APPLICATIONS[item][0]

UR_LOGIN = 'login'
UR_ARCHIVE = 'archive'
UR_REGENSITE = 'regensite'
#UR_UPLOAD = 'upload'
UR_EDIT = 'edit'
UR_CREATE = 'create'
UR_DELETE = 'delete'
UR_READ = 'read'
UR_DESIGN = 'design'
UR_MANAGE = 'manage'
UR_PUBLISH = 'publish'

UR_FUNCTIONS = { \
    UR_READ:['Read', UR_HAS_CHILDREN], \
    UR_EDIT:['Edit', UR_HAS_CHILDREN], \
    UR_CREATE:['Create', UR_HAS_CHILDREN], \
    UR_DELETE:['Delete', UR_HAS_CHILDREN], \
    UR_LOGIN:['Login', UR_NO_CHILDREN], \
    UR_ARCHIVE:['Archive', UR_NO_CHILDREN], \
    UR_REGENSITE:['Regen Site', UR_NO_CHILDREN], \
    UR_MANAGE:['Manage Site', UR_NO_CHILDREN], \
    UR_PUBLISH:['Publish', UR_HAS_CHILDREN], \
    UR_DESIGN:['Design Site', UR_NO_CHILDREN]}
#    UR_UPLOAD:['Upload Files', UR_NO_CHILDREN], \

UR_FUNCTIONS_PRETTY = dict()
ufkeys = UR_FUNCTIONS.keys()
ufkeys.sort()
for item in ufkeys:
    UR_FUNCTIONS_PRETTY[item] = UR_FUNCTIONS[item][0]

SEX_LIST = ['M', 'F']

ursemname = 'userrules'
usersemname = 'users'

def loadUserRules(filename):
    urCollection = None
    sem = Semaphore(ursemname)
    sem.put()
    userRulesProperties = PropertyDataParser(filename)
    sem.remove()
    if (userRulesProperties.hasProperty('rule')):
        rules = userRulesProperties.getPropertyAsList('rule')
        urCollection = UserRuleCollection(rules)
    return urCollection

def writeUserRules(urCollection, filename):
    '''Write the rules out to a properties file.'''
    pfb = PropertyFileBuilder()

    for rule in urCollection.rules:
        pfb.add('rule', rule)

    sem = Semaphore(ursemname)
    sem.put()
    pfb.write(filename)
    sem.remove()

def sendInviteEmail(fromUser, toUser):
    replaceDict = dict()
    replaceDict['fromEmail'] = fromUser.email
    replaceDict['toEmail'] = toUser.email
    replaceDict['problemEmail'] = 'problem@yakjive.com'
    replaceDict['subject'] = fromUser.first + ' has invited you to use YakJive.com'
    replaceDict['toName'] = toUser.first
    replaceDict['longFromName'] = fromUser.first + ' ' + fromUser.last
    replaceDict['shortFromName'] = fromUser.first
    replaceDict['rootURL'] = APPLICATION.rootURL
    replaceDict['adminURL'] = APPLICATION.adminURL
    replaceDict['username'] = toUser.username
    replaceDict['password'] = toUser.password
    replaceDict['penname'] = toUser.nickname
    replaceDict['code'] = 'S' + str(APPLICATION.ID)
    if (fromUser.sex == 'M'):
        replaceDict['fromSex'] = 'he'
    else:
        replaceDict['fromSex'] = 'she'
    if (fromUser.sex == 'M'):
        replaceDict['fromSexPossesive'] = 'his'
    else:
        replaceDict['fromSexPossesive'] = 'her'

    emailBody = readTextFile(FILENAME_EMAIL_INVITE, True, replaceDict)

    sendEmail(fromUser.email, toUser.email, emailBody)

#Classes
class UserRuleCollection:

    def __init__(self, rules = None):
        self.rules = rules
        self.frules = None
        self.fname = None

    def check(self, nickname, function, application = None, component = None):
        '''Check to see if a user has an exact rule.'''
        if ((self.frules is None) or (nickname != self.fname)):
            self.filter(nickname)
        if (component is not None):
            rule1 = nickname + '.' + function + '.' + application + '.' + component
        else:
            rule1 = 'invalid'
        if (application is not None):
            rule2 = nickname + '.' + function + '.' + application
        else:
            rule2 = 'invalid'
        rule3 = nickname + '.' + function

        check = ((rule1 in self.frules) or
            (rule2 in self.frules) or
            (rule3 in self.frules))
        return check

    def hasAny(self, nickname, application):
        '''Check to see if a user is allowed any functions on a particular application.'''
        frules = self.getFilteredRules(nickname)
        check = False
        for rule in frules:
            if (rule.find(application) > -1):
                check = True
                break
        return check

    def filter(self, nickname):
        self.frules = list(self.rules)
        items = list()
        for i in range(len(self.frules)):
            if (self.frules[i].find(nickname + '.') != 0):
                items += [i]
        items.reverse()
        for item in items:
            self.frules.pop(item)
        self.frules.sort()
        self.fname = nickname

    def getFilteredRules(self, nickname):
        if ((self.frules is None) or (nickname != self.fname)):
            self.filter(nickname)
        return self.frules

    def getRules(self):
        return self.rules

    def add(self, nickname, function = None, application = None, component = None):
        ''' Add values to the list of rules.  Either pass in the atomized rule
        parts or the whole rule as the first parameter.'''
        data = nickname
        if ((function is None) and (data.find('.') < 0)):
            raise 'Cannot add rule that is only a username.'
        if (function is not None):
            data += '.' + function
        if (application is not None):
            data += '.' + application
        if (component is not None):
            data += '.' + component
        self.rules += [data]
        self.frules = None
        self.fname = None

    def delete(self, nickname, function = None, application = None, component = None):
        ''' Delete values from the list of rules.  Either pass in the atomized rule
        parts or the whole rule as the first parameter.'''
        data = nickname
        if (function is not None):
            data += '.' + function
        if (application is not None):
            data += '.' + application
        if (component is not None):
            data += '.' + component
        items = list()
        for item in range(len(self.rules)):
            if (self.rules[item].find(data) == 0):
                items += [item]
        items.reverse()
        for item in items:
            self.rules.pop(item)
        self.frules = None
        self.fname = None

    def deleteByComponent(self, component):
        ''' Delete all rules from the database that have components with the
        given value.'''
        data = '.' + component
        baddata = '.' + component + '.'
        items = list()
        for item in range(len(self.rules)):
            if ((self.rules[item].find(data) > 0) \
                    and (self.rules[item].find(baddata) == -1)):
                items += [item]
        items.reverse()
        for item in items:
            self.rules.pop(item)
        self.frules = None
        self.fname = None

    def replaceNickname(self, oldName, newName):
        ''' Used when users are logging in for the first time and wish to change their
        nickname.  Takes an old nickname and replaces it with a new one.'''
        for i in range(len(self.rules)):
            data = self.rules[i].split('.')

            if (data[0] == oldName):
                data[0] = newName
            if ((len(data) == 4) and (data[3] == oldName)):
                data[3] = newName

            self.rules[i] = join(data, '.')

class User:
    #Constructor
    def __init__(self):
        self.first = ''
        self.last = ''
        self.email = ''
        self.nickname = ''
        self.username = ''
        self.password = ''
        randchars = ''
        for i in range(10):
           randchars += chr(randint(65,90))
           randchars += chr(randint(97,122))
           randchars += chr(randint(48,57))
        self.key = randchars
        self.id = -1
        self.bio = ''
        self.active = True
        self.webmaster = False

        self.photo = None
        self.sex = 'M'
        self.birthYear = 1900
        self.privateProfile = True
        self.showWizard = True
        self.hasLoggedIn = True

    def checkLikeness(self, user):
        ''' Returns None if there is no likeness between user and this instance. '''
        data = ''
        if ((user.first == self.first) and (user.last == self.last)):
            data += 'Same FIRST and LAST names. '
        if (user.nickname == self.nickname):
            data += 'Same NICKNAME. '
        if (user.username == self.username):
            data += 'Same USERNAME. '
        if (data == ''):
            data = None
        return data

class UserCollection:

    def __init__(self, users):
        self.users = users
        self.sorted = False

    def getUsers(self):
        if (not self.sorted):
            for i in range(len(self.users)):
                for j in range(i+1, len(self.users)):
                    if (self.users[i].id > self.users[j].id):
                        t = self.users[j]
                        self.users[j] = self.users[i]
                        self.users[i] = t
                        self.sorted = True
        return self.users

    def add(self, newuser):
        maxId = 0
        for user in self.users:
            if (user.id > maxId):
                maxId = user.id
            check = user.checkLikeness(newuser)
            if (check is not None):
                raise check
        newuser.id = maxId + 1
        self.sorted = False
        self.users += [newuser]

    def delete(self, id):
        ind = -1
        for i in range(len(self.users)):
            if (self.users[i].id == id):
                ind = i
                break
        self.users.pop(ind)

    def getUserByNickname(self, nickname):
        user = None
        for usr in self.users:
            if (usr.nickname == nickname):
                user = usr
                break
        return user

    def getUserById(self, id):
        user = None
        for usr in self.users:
            if (usr.id == id):
                user = usr
                break
        return user

    def getUserByKey(self, key):
        user = None
        for usr in self.users:
            if (usr.key == key):
                user = usr
                break
        return user

    def getUserByUsername(self, username):
        user = None
        for usr in self.users:
            if (usr.username == username):
                user = usr
                break
        return user

class UserDataWriter:
    """ A class to write the user properties file. """

    def __init__(self, users):
        self.users = users

    def build(self):
        data = '<?xml version="1.0"?>\n'
        data += '<users>\n'
        if ((self.users is None) or (len(self.users) == 0)):
            raise 'No users to write to file.'
        for user in self.users:
            data += '\t<user'
            data += ' id="' + str(user.id) + '"'
            data += ' first="' + user.first + '"'
            data += ' last="' + user.last + '"'
            data += ' nickname="' + user.nickname + '"'
            data += ' email="' + user.email + '"'
            data += ' username="' + user.username + '"'
            data += ' password="' + user.password + '"'
            data += ' key="' + user.key + '"'
            if (user.showWizard):
                data += ' showWizard="True"'
            else:
                data += ' showWizard="False"'
            #data += ' bio="' + user.bio + '"'
            if (user.privateProfile):
                data += ' private="True"'
            else:
                data += ' private="False"'
            if (user.webmaster):
                data += ' webmaster="True"'
            if (user.active):
                data += ' active="True"'
            else:
                data += ' active="False"'
            # Don't bother indicating that the user has logged if True
            if (not user.hasLoggedIn):
                data += ' hasLoggedIn="False"'
            data += '>\n'
            if (user.bio != ''):
                data += '\t<bio><![CDATA[' + user.bio + ']]></bio>\n'
            data += '\t<sex>' + user.sex + '</sex>\n'
            data += '\t<birthYear>' + str(user.birthYear) + '</birthYear>\n'
            if (user.photo is not None):
                data += '\t' + user.photo.toXML() + '\n'
            data += '</user>\n'
        data += '</users>\n'
        return data

    def write(self, filename):

        sem = Semaphore(usersemname)
        sem.put()
        data = self.build()
        f = file(filename, 'w')
        f.write(data)
        f.flush()
        f.close()
        sem.remove()

class UserDataParser:
    """A user data file parsing class used to load and process
xml files that can be considered application user
files.  Files should have the following simple
form:

     <?xml version="1.0"?>
    <users>
        <user first="Chris" last="Andrews" nickname="MgEd" email="chris@someserver.org" username="chris" password="chris" key="dfsadfasdf"/>
        <user first="Noah" last="Smith" nickname="AssocEd2" email="noah@someserver.cc" username="noah" password="noah" key="sadfsdfsdaf"/>
    </users>
"""

    #Constructor
    def __init__(self, filename):
        """Initialze the class with a file name relative to the path of the root script."""
        sem = Semaphore(usersemname)
        sem.put()
        try:
            self.users = None
            f = file(filename)
            data = f.read()
            f.close()
            self.parse(data)
        except IOError:
            sem.remove()
            raise "IOError attempting to access:", filename
        sem.remove()

    def __processStartElement__(self, name, attrs):
        if (name == 'user'):
            user = User();
            user.first = str(attrs['first'])
            user.last = str(attrs['last'])
            user.email = str(attrs['email'])
            user.nickname = str(attrs['nickname'])
            user.username = str(attrs['username'])
            user.password = str(attrs['password'])
            user.key = str(attrs['key'])
            user.id = int(attrs['id'])
            if ('active' in attrs):
                user.active = (attrs['active'] in TRUE)
            if ('showWizard' in attrs):
                user.showWizard = (attrs['showWizard'] in TRUE)
            user.webmaster = False
            if ('webmaster' in attrs):
                user.webmaster = (attrs['webmaster'] in TRUE)
            if ('private' in attrs):
                user.privateProfile = (attrs['private'] in TRUE)
            if ('hasLoggedIn' in attrs):
                user.hasLoggedIn = (attrs['hasLoggedIn'] in TRUE)

            if (self.users is None):
                self.users = []
            self.users += [user]
            self.currentuser = user
        elif (name == 'attachment'):
            attachment = Attachment()
            attachment.name = attrs['name']
            attachment.origName = attrs['origName']
            attachment.notes = attrs['notes']
            attachment.align = attrs['align']
            attachment.isImg = (attrs['isImg'] in TRUE)
            attachment.imgHeight = int(attrs['imgHeight'])
            attachment.imgWidth = int(attrs['imgWidth'])
            attachment.size = int(attrs['size'])
            self.currentuser.photo = attachment
        self.currentproperty = name

    def __processNewsItemCharData__(self, data):
        if ((self.currentproperty is not None) and \
                (str(data).strip() != '')):
            if (self.currentproperty == 'bio'):
                self.currentuser.bio = data
            if (self.currentproperty == 'birthYear'):
                self.currentuser.birthYear = int(data)
            if (self.currentproperty == 'sex'):
                self.currentuser.sex = data

    #Parse the data into a properties dictionary
    def parse(self, data):
        userParser = xml.parsers.expat.ParserCreate()
        userParser.StartElementHandler = self.__processStartElement__
        userParser.CharacterDataHandler = self.__processNewsItemCharData__
        userParser.Parse(data)
        return self.users

    def count(self):
        return len(self.users)

    #Return the list if you want the whole thing
    def getUsers(self):
        return self.users

    def getUserCollection(self):
        return UserCollection(self.users)

    def getUser(self, nickname):
        '''Get the user by nickname.'''
        data = None
        for item in self.users:
            if (str(item.nickname) == str(nickname)):
                data = item
                break
        return data

    def getBlogPageName(cls, nickname):
        safename = ''
        for c in nickname:
            if (c in ALPHANUM_CHARS.strip()):
                safename += c
            else:
                safename += '-'
        return str(safename + '-blog')

    # TODO-L: If server converts to Python 2.4, change to function decorator
    getBlogPageName = classmethod(getBlogPageName)

    def login(self, username, password):
        '''Return the key if the user is good, return None otherwise.'''
        data = None
        for user in self.users:
            if ((user.active) and (user.username == username) and (user.password == password)):
               data = user.key
               break
        return data

    def unlock(self, key):
        '''Return the nickname if the key is good, return None otherwise.'''
        data = None
        for user in self.users:
            if ((user.active) and (user.key == key)):
               data = user.nickname
               break
        return data




