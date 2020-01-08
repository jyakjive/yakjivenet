# Imports
from util.properties import *
from util.fileutils import Semaphore
from newscommunity.ncvars import *

# Declarations
semname = 'newsletter'

# Definitions

def loadNewsletterData(filename):
    '''Create a new dictionary of news sections by passing
    in a file name to the section properties file.'''

    sem = Semaphore(semname)
    sem.put()

    parser = PropertyDataParser(filename)

    sem.remove()

    recipients = list()

    if (parser.hasProperty('recipient')):
        for i in range(0, len(parser.getPropertyAsList('recipient'))):
            attrs = parser.getPropertyAttrsAsList('recipient')[i]

            nr = NewsletterRecipient()
            nr.name= attrs['name']
            nr.email= attrs['email']

            recipients += [nr]

    return recipients

def writeNewsletterData(filename, recipients):
    '''Write the sections properties file.'''

    pfb = PropertyFileBuilder()

    for recipient in recipients:
        pfb.add('recipient', recipient.name, \
            recipient.getAttrDict())

    sem = Semaphore(semname)
    sem.put()

    pfb.write(filename)

    sem.remove()

class NewsletterRecipient:

    def __init__(self, name = '', email = ''):
        self.name = name
        self.email = email

    def getAttrDict(self):
        data = dict()

        data['name'] = self.name
        data['email'] = self.email

        return data