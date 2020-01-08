# Imports
from util.properties import *
from util.fileutils import Semaphore
from newscommunity.ncvars import *

# Declarations
semname = 'infoPageSem'

# Definitions

def loadInfoPages(filename):
    '''Create an InfoPages object by passing
    in a file name to the style properties file.'''

    sem = Semaphore(semname)
    sem.put()

    parser = PropertyDataParser(filename)

    sem.remove()

    pages = InfoPages()

    for propList in parser:
        prop = propList[0]

        ip = InfoPage()

        ip.name = prop.name
        ip.content = prop.content

        ip.order = int(prop.attrs['order'])
        ip.isVisible = (prop.attrs['visible'] in TRUE)
        ip.title = str(prop.attrs['title'])
        ip.subtitle = str(prop.attrs['subtitle'])
        if ('menuName' in prop.attrs):
            ip.menuName = str(prop.attrs['menuName'])
        if ('filename' in prop.attrs):
            ip.filename = str(prop.attrs['filename'])

        pages.add(ip)

    return pages

def writeInfoPages(filename, infoPages):
    '''Write the info pages properties file.'''

    pfb = PropertyFileBuilder()
    pfb.setCData(True)

    for item in infoPages:
        pfb.add(item.name, item.content, item.getAttrDict())

    sem = Semaphore(semname)
    sem.put()

    pfb.write(filename)

    sem.remove()

# Classes
class InfoPage:

    def __init__(self):
        self.order = -1
        self.isVisible = True
        self.title = ''
        self.subtitle = ''
        self.content = ''
        self.name = ''
        self.filename = ''
        self.menuName = ''

    def getAttrDict(self):
        data = dict()
        data['order'] = self.order
        data['visible'] = self.isVisible
        data['title'] = self.title
        data['subtitle'] = self.subtitle
        data['menuName'] = self.menuName
        if (self.filename <> ''):
            data['filename'] = self.filename
        return data

class InfoPages:

    def __init__(self):
        self.pages = dict()

    def add(self, page):
        self.remove(page.name)
        self.pages[page.name] = page

    def remove(self, name):
        if (name in self.pages):
            del self.pages[name]

    def get(self, name):
        data = None
        if (name in self.pages):
            data = self.pages[name]
        return data

    def __len__(self):
        return len(self.pages)

    def __iter__(self):
        self.index = 0
        return self

    def next(self):
        data = None

        if (self.index == len(self.pages)):
            raise StopIteration

        for page in self.pages:
            if (self.pages[page].order == self.index):
                data = self.pages[page]
                break
        self.index += 1
        return data