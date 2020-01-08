# imports

from newscommunity.ncvars import *
from newscommunity.application import APPLICATION
from classes.application_handler import *
from util.fileutils import getMultiDirTreeSize

# definitions

def getStorageRatio():
    dirs = [APPLICATION.dataDirectory, APPLICATION.newsFileLocation]
    spaceUsed = getMultiDirTreeSize(dirs)
    pct = 1.0 * spaceUsed / SITE_TYPE_SIZE[APPLICATION.siteType]
    return pct

def getStoragePercent():
    pct = 100.0 * getStorageRatio()
    return pct

def getStorageMessage(pct):
    data = ''
    if (pct >= 100):
        # TODO: Add in upgrade link
        data = 'Your site has reached the total space allowed.<br>' + \
                'You will not be able to add new content until you remove some existing content or upgrade your site.'
    elif (pct > 95):
        data = 'Your site using more than 95% of the space available!'

    return data

def checkStorage():
    s = Storage()

    s.percent = getStoragePercent()
    s.message = getStorageMessage(s.percent)
    s.locked = (s.percent >= 100)

    if (s.locked != APPLICATION.storageLocked):
        APPLICATION.storageLocked = s.locked
        writeApplication(FILENAME_APPLICATION, APPLICATION)

    return s

# classes

class Storage:
    def __init__(self):
        self.percent = 0
        self.message = ''
        self.locked = False
