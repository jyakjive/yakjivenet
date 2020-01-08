#Imports
import string
import xml.parsers.expat
from util.properties import *
from util.fileutils import Semaphore
from newscommunity.ncvars import *

#Declarations

semname = 'page'

def loadNewsPageProperties(filename):
    '''Create a new dictionary of news pages by passing in a file name to the page properties file.'''

    sem = Semaphore(semname)
    sem.put()

    parser = PropertyDataParser(filename)

    sem.remove()

    pages = NewsPageDict()

    for i in range(0, len(parser.getPropertyAsList('page'))):
        attrs = parser.getPropertyAttrsAsList('page')[i]

        name = parser.getPropertyAsList('page')[i]
        title = attrs['title']
        headlineType = attrs['headlineType']
        pageType = attrs['pageType']
        # TODO-L: refactor 'newspage' to be 'section'
        newspage = attrs['newspage']
        column = attrs['column']
        displayNum = attrs['displayNum']
        rank = attrs['rank']
        isVisible = 'True'
        if ('isVisible' in attrs):
            isVisible = attrs['isVisible']
        pageOwner = None
        if ('pageOwner' in attrs):
            pageOwner = attrs['pageOwner']
        isBlog = 'False'
        if ('isBlog' in attrs):
            isBlog = attrs['isBlog']
        expires = 'Never'
        if ('expires' in attrs):
            if (attrs['expires'] == 'Never'):
                expires = 'Never'
            else:
                expires = int(attrs['expires'])

        # TODO-L: Changes this to a zero-arg constructor
        newsPage = NewsPage(
            name,
            title,
            headlineType,
            pageType,
            newspage,
            column,
            displayNum,
            rank,
            isVisible,
            pageOwner,
            isBlog,
            expires)

        if ('id' in attrs):
            newsPage.id = int(attrs['id'])
        if ('active' in attrs):
            newsPage.active = (attrs['active'] in TRUE)
        if ('feedback' in attrs):
            newsPage.feedback = (attrs['feedback'] in TRUE)
        if ('rating' in attrs):
            newsPage.rating = attrs['rating']
        if ('attachments' in attrs):
            newsPage.attachments = (attrs['attachments'] in TRUE)
        if ('subTitle' in attrs):
            newsPage.subTitle = attrs['subTitle']
        if ('sortType' in attrs):
            newsPage.sortType = attrs['sortType']
            if (newsPage.sortType == 'date'):
                newsPage.sortType = 'date: newest first'
        if ('promptComments' in attrs):
            newsPage.promptComments = attrs['promptComments']
        if ('allowComments' in attrs):
            newsPage.allowComments = (attrs['allowComments'] in TRUE)

        pages[parser.getPropertyAsList('page')[i]] = newsPage

    return pages

def writeNewsPageProperties(pages, filename):
    '''Write the news pages out to a properties file.'''
    pfb = PropertyFileBuilder()

    for page in pages:
        pfb.add('page', pages[page].name, pages[page].getAttrDict())


    sem = Semaphore(semname)
    sem.put()

    pfb.write(filename)

    sem.remove()

def getRankDict(pages):
    rankDict = dict()
    for page in pages:
        rankDict[pages[page].rank] = page
    return rankDict

def deletePage(pages, editPage):
    # Remove the item from the dictionary
    del pages[editPage]

    # Re-rank the remaining items in order
    rankDict = dict()
    for page in pages:
        rankDict[pages[page].rank] = page
    rankKeys = rankDict.keys()
    rankKeys.sort()
    rankCount = 0

    for r in rankKeys:
        pages[rankDict[r]].rank = rankCount
        rankCount += 1

    writeNewsPageProperties(pages, FILENAME_PAGES)

    return pages



#Classes

class NewsPage:
    '''An object that encapsulates the properties of a news page.'''

    def __init__(self, name = '', title = '', headlineType = '', pageType = '', newspage = '', column = 0, \
            displayNum = 0, rank = -1, isVisible = 'True', pageOwner = '', isBlog = 'False', \
            expires = 'Never', sortType = SORT_DATE, subTitle = ''):
        '''Create a new NewsPage'''
        # TODO: make this a real zero-arg constructor

        self.name = name
        self.id = -1
        self.title = title
        self.subTitle = subTitle
        self.headlineType = headlineType
        self.pageType = pageType

        # TODO-R: This should be SECTION not NEWSPAGE
        self.newspage = newspage

        self.column = int(column)
        self.displayNum = int(displayNum)
        self.rank = int(rank)
        self.isVisible = (isVisible in TRUE)
        self.pageOwner = pageOwner
        self.isBlog = (isBlog in TRUE)
        if (expires == 'Never'):
            self.expires = expires
        else:
            self.expires = int(expires)
        self.active = True # can be updated
        # TODO: Implement rating functionality
        self.rating = None # None, Priority (H,M,L), Ten (1..10), Five (1..5), A..E
        # DONE?: Implement attachment check in add_news.py and add_url.py
        self.attachments = True # allow attachments
        self.sortType = sortType

        self.promptComments = 'add a comment'
        self.allowComments = False

        # DEPRECATED: in favor of allowComments
        self.feedback = False # allow feedback

        self.articleCount = 0
        self.pendingArticleCount = 0
        self.articlesLastModified = None

    def getAttrDict(self):
        data = dict()
        data['title'] = self.title
        data['id'] = str(self.id)
        data['subTitle'] = self.subTitle
        data['headlineType'] = self.headlineType
        data['pageType'] = self.pageType
        data['newspage'] = self.newspage
        data['column'] = self.column
        data['displayNum'] = self.displayNum
        if (self.isVisible in TRUE):
            data['isVisible'] = 'True'
        else:
            data['isVisible'] = 'False'
        if (self.isBlog in TRUE):
            data['isBlog'] = 'True'
        else:
            data['isBlog'] = 'False'
        data['pageOwner'] = self.pageOwner
        data['rank'] = self.rank
        data['expires'] = self.expires
        if (self.active in TRUE):
            data['active'] = 'True'
        else:
            data['active'] = 'False'
        data['feedback'] = self.feedback
        data['rating'] = self.rating
        data['sortType'] = self.sortType
        data['attachments'] = self.attachments
        data['promptComments'] = self.promptComments
        if (self.allowComments in TRUE):
            data['allowComments'] = 'True'
        else:
            data['allowComments'] = 'False'

        data['articleCount'] = self.articleCount
        data['pendingArticleCount'] = self.pendingArticleCount
        data['articlesLastModified'] = self.articlesLastModified
        return data

    def toString(self):
        data = 'NewsPage instance:'
        data += '\tname: '+ self.name + '\n'
        data += '\tid: '+ self.id + '\n'
        data += '\ttitle: '+ str(self.title) + '\n'
        data += '\tsubTitle: '+ str(self.subTitle) + '\n'
        data += '\theadlineType: '+ self.headlineType + '\n'
        data += '\tpageType: ' + self.pageType + '\n'
        data += '\tnewspage: ' + str(self.newspage) + '\n'
        data += '\tcolumn: ' + str(self.column) + '\n'
        data += '\tdisplayNum: ' + str(self.displayNum) + '\n'
        data += '\tisVisible: ' + str(self.isVisible) + '\n'
        data += '\tpageOwner: ' + str(self.pageOwner) + '\n'
        data += '\tisBlog: ' + str(self.isBlog) + '\n'
        data += '\trank: ' + str(self.rank) + '\n'
        data += '\texpires: ' + str(self.expires) + '\n'
        data += '\tactive: ' + str(self.active) + '\n'
        data += '\tfeedback: ' + str(self.feedback) + '\n'
        data += '\trating: ' + str(self.rating) + '\n'
        data += '\tattachments: ' + str(self.attachments) + '\n'
        data += '\tsortType: ' + str(self.sortType) + '\n'
        data += '\tpromptComments: ' + str(self.promptComments) + '\n'
        data += '\tallowComments: ' + str(self.allowComments) + '\n'
        data += '\n'
        return data

class NewsPageDict (dict):
    __referenceInstance__ = NewsPage()

    def countBySection(self, sectionName):
        c = 0
        for item in self:
            if (self[item].newspage == sectionName):
                c += 1
        return c

    def __setitem__(self, key, value):
        dict.__setitem__(self, key, value)
        if (type(value) != type(NewsPageDict.__referenceInstance__)):
            raise 'Illegal type ' + str(type(value)) + ' passed to NewsPageDict'
        if (value.id == -1):
            value.id = self.getMaxID() + 1
            value.rank = self.getMaxRank() + 1

    def getByID(self, id):
        '''Get page matching the id.'''
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

    def getMaxRank(self):
        '''Get the highest rank of any newspage in the dict.'''
        c = -1
        for item in self:
            if (self[item].rank > c):
                c = self[item].rank
        return c