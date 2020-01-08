
# imports
from util.properties import *
from vars import *
from util.fileutils import Semaphore
from newscommunity.ncvars import TRUE

# declarations
semname = 'sitesem'

# definitions
def loadSites(filename):
    '''Create a new dictionary of sites by passing
    in a file name to the section properties file.'''

    sem = Semaphore(semname)
    sem.put()

    parser = PropertyDataParser(filename)

    sem.remove()

    sites = SiteDict()

    for i in range(0, len(parser.getPropertyAsList('site'))):
        attrs = parser.getPropertyAttrsAsList('site')[i]

        site = Site()
        site.domain = parser.getPropertyAsList('site')[i]

        site.id = int(attrs['id'])
        site.contactEmail = attrs['contactEmail']
        site.webmasterUsername = attrs['webmasterUsername']
        site.webmasterFirst = attrs['webmasterFirst']
        site.webmasterLast = attrs['webmasterLast']
        site.dateCreated = attrs['dateCreated']
        site.activated = (attrs['activated'] in TRUE)
        site.activationCode = attrs['activationCode']
        site.inviteCode = attrs['inviteCode']
        site.status = attrs['status']
        site.rootWWWDir = attrs['rootWWWDir']
        site.rootAdminDir = attrs['rootAdminDir']

        sites[site.domain] = site

    return sites

def writeSites(filename, sites):
    '''Write the sites properties file.'''

    pfb = PropertyFileBuilder()

    for site in sites:
        pfb.add('site', sites[site].domain, sites[site].getAttrDict())

    sem = Semaphore(semname)
    sem.put()
    pfb.write(filename)
    sem.remove()

# classes
class Site:
    ''' A YakJive user website account. '''
    def __init__(self):
        self.id = -1
        self.contactEmail = ''
        self.webmasterUsername = ''
        self.webmasterFirst = ''
        self.webmasterLast = ''
        self.dateCreated = None
        self.activated = False
        self.domain = ''
        self.activationCode = ''
        self.inviteCode = ''
        self.status = STATUS_GOOD
        self.rootWWWDir = ''
        self.rootAdminDir = ''

    def getAttrDict(self):
        data = dict()
        data['id'] = self.id
        data['dateCreated'] = self.dateCreated
        data['contactEmail'] = self.contactEmail
        data['webmasterFirst'] = self.webmasterFirst
        data['webmasterLast'] = self.webmasterLast
        data['webmasterUsername'] = self.webmasterUsername
        data['activationCode'] = self.activationCode
        data['inviteCode'] = self.inviteCode
        data['status'] = self.status
        data['rootWWWDir'] = self.rootWWWDir
        data['rootAdminDir'] = self.rootAdminDir
        if (self.activated):
            data['activated'] = 'True'
        else:
            data['activated'] = 'False'
        return data

class SiteDict(dict):
    ''' Dictionary class for holding site objects. '''
    __referenceInstance__ = Site()

    def __setitem__(self, key, value):
        dict.__setitem__(self, key, value)
        if (type(value) != type(SiteDict.__referenceInstance__)):
            raise 'Illegal type ' + str(type(value)) + ' passed to SiteDict'
        if (value.id == -1):
            value.id = self.getMaxID() + 1

    def getByID(self, id):
        '''Get site matching the id.'''
        data = None
        try:
            for item in self:
                if (self[item].id == int(id)):
                    data = self[item]
                    break
        except:
            pass
        return data

    def getMaxID(self):
        '''Get the highest id of any newspage in the dict.'''
        c = -1
        for item in self:
            if (self[item].id > c):
                c = self[item].id
        return c