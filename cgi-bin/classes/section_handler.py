# Imports
from util.properties import *
from util.fileutils import Semaphore
from newscommunity.ncvars import *
from newspage_handler import getRankDict
from newscommunity.application import APPLICATION

# Declarations
semname = 'sectSem'

# Definitions

# TODO-L: refactor all over to remove loadSections and use loadSectionList
def loadSections(filename):
    '''Create a new dictionary of news sections by passing
    in a file name to the section properties file.'''

    sem = Semaphore(semname)
    sem.put()

    parser = PropertyDataParser(filename)

    sem.remove()

    sections = dict()

    for i in range(0, len(parser.getPropertyAsList('section'))):
        attrs = parser.getPropertyAttrsAsList('section')[i]

        section = Section()
        section.name = parser.getPropertyAsList('section')[i]
        section.longname = attrs['longname']

        if ('isHomepage' in attrs):
            section.isHomepage = (attrs['isHomepage'] in TRUE)
        if ('columns' in attrs):
            section.columns = int(attrs['columns'])
        if ('order' in attrs):
            section.order = int(attrs['order'])
        if ('isActive' in attrs):
            section.isActive = (attrs['isActive'] in TRUE)
        if ('isVisible' in attrs):
            section.isVisible = (attrs['isVisible'] in TRUE)

        sections[section.name] = section

    return sections

def loadSectionList(filename):
    '''Create a new dictionary of news sections by passing
    in a file name to the section properties file.'''

    sem = Semaphore(semname)
    sem.put()

    parser = PropertyDataParser(filename)

    sem.remove()

    sectionList = SectionList()

    for i in range(0, len(parser.getPropertyAsList('section'))):
        attrs = parser.getPropertyAttrsAsList('section')[i]

        section = Section()
        section.name = parser.getPropertyAsList('section')[i]
        section.longname = attrs['longname']

        if ('isHomepage' in attrs):
            section.isHomepage = (attrs['isHomepage'] in TRUE)
        if ('columns' in attrs):
            section.columns = int(attrs['columns'])
        if ('order' in attrs):
            section.order = int(attrs['order'])
        if ('isActive' in attrs):
            section.isActive = (attrs['isActive'] in TRUE)
        if ('isVisible' in attrs):
            section.isVisible = (attrs['isVisible'] in TRUE)

        sectionList.add(section)

    return sectionList

def writeSections(filename, sections):
    '''Write the sections properties file.'''

    pfb = PropertyFileBuilder()

    # TODO-L: Remove next line when refactored to use only loadSectionList
    sectionList = buildSectionList(sections)

    for section in sectionList:
        pfb.add('section', section.name, section.getAttrDict())

    sem = Semaphore(semname)
    sem.put()

    pfb.write(filename)

    sem.remove()

def buildSectionList(sections):
    sectionList = SectionList()
    for item in sections:
        sectionList.add(sections[item])
    return sectionList

def getHomepageSection(sections):
    '''Get the name of the section that is the homepage.'''
    data = ''
    for item in sections:
        if (sections[item].isHomepage):
            data = item
            break
    return data

# TODO: Allow the caller to pass in the current page name to change the behavior of that page name in the menu
def createSectionMenu(sections, pages):
    # TODO: DEPRECATE this method.  Replaced by the MenuBuilder.
    raise 'DEPRECATION ERROR: createSectionMenu is DEPRECATED'
#    rankDict = getRankDict(pages)
#    rankKeys = rankDict.keys()
#    rankKeys.sort()
#
#    sectionList = buildSectionList(sections)
#
#    homepageSection = getHomepageSection(sections)
#    sectionMenu = ''
#    for section in sectionList:
#        if (section.isVisible):
#            usedpages = 0
#            for rKey in rankKeys:
#                page = rankDict[rKey]
#                if (pages[page].newspage == section.name):
#                    if (pages[page].isVisible == True):
#                        usedpages += 1
#            if (usedpages > 0):
#                if (sectionMenu != ''):
#                    sectionMenu += ' <span class="sectionMenu">' + APPLICATION.menuSeparator + '</span> '
#
#                if (section.name != homepageSection):
#                    sectionMenu += '<span class="sectionMenu">' + \
#                        '<a href="' + section.name + '.html" title="Go to the ' + \
#                        section.longname + ' section">' + \
#                        section.longname + '</a></span>'
#                else:
#                    sectionMenu += '<span class="sectionMenu">' + \
#                        '<a href="index.html" title="Go to the main page section">Home</a></span>'
#    return sectionMenu

# Classes
class Section:

    def __init__(self):
        self.name = ''
        self.longname = ''
        self.isHomepage = False
        self.isActive = True
        self.isVisible = True
        self.columns = 3
        self.order = -1

    def getAttrDict(self):
        data = dict()
        data['longname'] = self.longname
        data['columns'] = self.columns
        data['order'] = self.order
        if (self.isHomepage):
            data['isHomepage'] = 'True'
        else:
            data['isHomepage'] = 'False'
        if (self.isActive):
            data['isActive'] = 'True'
        else:
            data['isActive'] = 'False'
        if (self.isVisible):
            data['isVisible'] = 'True'
        else:
            data['isVisible'] = 'False'
        return data

    def copy(self):
        c = Section()
        c.name = self.name
        c.longname = self.longname
        c.isHomepage = self.isHomepage
        c.isActive = self.isActive
        c.isVisible = self.isVisible
        c.columns = self.columns
        c.order = self.order
        return c

class SectionList:
    def __init__(self):
        self.sections = list()
        self.sectionNames = list()
        self.index = 0
        self.isSorted = False

    def add(self, section):
        self.sections += [section]
        self.sectionNames += [section.name]
        self.isSorted = False

    def keys(self):
        return self.sectionNames

    def get(self, name):
        data = None
        for i in range(len(self.sectionNames)):
            item = self.sectionNames[i]
            if (item == name):
                data = self.sections[i]
        return data

    def moveUp(self, name):
        self.sort()
        item1 = self.get(name)

        if (item1.order != 0):
            item2 = None
            for oitem in self.sections:
                if (oitem.order == (item1.order - 1)):
                    item2 = oitem
                    break

            if (item2 is not None):
                item1.order = item1.order - 1
                item2.order = item2.order + 1

            self.isSorted = False

    def moveDown(self, name):
        self.sort()
        item1 = self.get(name)

        if (item1.order != (len(self.sections) - 1)):
            item2 = None
            for oitem in self.sections:
                if (oitem.order == (item1.order + 1)):
                    item2 = oitem
                    break

            if (item2 is not None):
                item1.order = item1.order + 1
                item2.order = item2.order - 1

            self.isSorted = False

    def sort(self):
        if (not self.isSorted):
            t = None
            # Sort by order
            for i in range(len(self.sections) - 1):
                for j in range(i + 1, len(self.sections)):
                    if (self.sections[i].order > self.sections[j].order):
                        t = self.sections[j]
                        self.sections[j] = self.sections[i]
                        self.sections[i] = t
                        t = self.sectionNames[j]
                        self.sectionNames[j] = self.sectionNames[i]
                        self.sectionNames[i] = t

            # Make sure the orders are sequential
            for i in range(len(self.sections)):
                self.sections[i].order = i

        self.isSorted = True

    def count(self):
        return len(self.sections)

    def copy(self):
        c = SectionList()
        for item in self:
            c.add(item.copy())
        return c

    def remove(self, name):
        index = -1
        for i in range(len(self.sectionNames)):
            item = self.sectionNames[i]
            if (item == name):
                index = i
        if (i > -1):
            del(self.sections[i])
            del(self.sectionNames[i])
            self.isSorted = False

    def __iter__(self):
        self.index = 0
        self.sort()
        return self

    def next(self):
        if (self.index == len(self.sections)):
            raise StopIteration
        data = self.sections[self.index]
        self.index += 1
        return data

