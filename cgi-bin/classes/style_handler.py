# Imports
from util.properties import *
from util.fileutils import Semaphore
from newscommunity.ncvars import *

# Declarations
semname = 'styleSem'

# Definitions

def loadStyles(filename):
    '''Create a new dictionary of news styles by passing
    in a file name to the style properties file.'''

    sem = Semaphore(semname)
    sem.put()

    parser = PropertyDataParser(filename)

    sem.remove()

    styles = dict()

    for i in range(0, len(parser.getPropertyAsList('style'))):
        attrs = parser.getPropertyAttrsAsList('style')[i]

        style = Style()
        style.name = parser.getPropertyAsList('style')[i]

        style.id = int(attrs['id'])
        style.prettyName = attrs['prettyName']
        style.menuType = attrs['menuType']

        styles[style.name] = style

    return styles

def writeStyles(filename, styles):
    '''Write the styles properties file.'''

    pfb = PropertyFileBuilder()

    for style in styles:
        pfb.add('style', styles[style].name, styles[style].getAttrDict())

    sem = Semaphore(semname)
    sem.put()

    pfb.write(filename)

    sem.remove()

def loadStyleText(filename):
    data = ''
    try:
        f = file(filename)
        data = f.read()
        f.close()
    except IOError:
        raise "IOError attempting to access:", filename

    return data

def getStyleFileName(key):
    data = key.split('.')
    name = data[len(data) - 1] + '.css'
    return name

# Classes
class Style:

    def __init__(self):
        self.name = ''
        self.prettyName = ''
        self.menuType = 'h' # h or v
        id = -1

    def getAttrDict(self):
        data = dict()
        data['id'] = self.id
        data['name'] = self.name
        data['prettyName'] = self.prettyName
        data['menuType'] = self.menuType
        return data
