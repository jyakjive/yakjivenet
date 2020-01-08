
# imports

from newscommunity.ncvars import *
from newscommunity.application import APPLICATION
from article_handler import *
#from article import *
from math import floor
from db.article_dao import *

# declarations

# definitions

def indexOfArticle(article, articles):
    count = 0
    for art in articles:
        if (article.id == art.id):
            break
        count += 1
    return count

def getArticlePageName(page, articles, article, dateDMY = None):
    ''' Get the filename for the HTML file that contains a particular
        article.
        # TODO: Consider breaking up alphabetical pages by A, B, C... so that you
        can reference them directly in a permalink.

        page - NewsPage object
        niList - NewsItemList object
        article - NewsItem object in the NewsItemList
        dateDMY - Day, Month, Year tuple from NewsItemList..getFirstSorted()
           Choosing not to bury this here because a whole lot of sorting would
           be going on.
    '''
    pageURL = APPLICATION.rootURL + page.name
    if (page.pageType == PAGE_LONG_ARTICLES):
        pageURL += '-' + str(article.id)
    elif (page.sortType in [SORT_DATE, SORT_DATE_REVERSE]):
        if (dateDMY is None):
            raise Exception('dateDMY cannot be None')

        if ((dateDMY[1] != article.publishedDate.timetuple()[1]) or (dateDMY[2] != article.publishedDate.timetuple()[0])):
            pageURL += str(int(article.publishedDate.timetuple()[1])) + '-' + (str(article.publishedDate.timetuple()[0])[2:])
    else:
        temp = int(floor(indexOfArticle(article, articles)/ITEMS_PER_PAGE))
        if (temp > 0):
            pageURL += str(temp)
    pageURL += '.html'
    return pageURL

# classes

class BriefArticle:
    def __init__(self):
        self.newspage = ''
        self.uid = -1
        # Note that this is the last-modified date
        self.date = None
        self.prettyDate = ''
        self.prettyModifiedDate = ''
        self.title = ''

    def setDate(self, year, month, day, hour, minute):
        self.date = time.strptime(
            str(year) + ' ' +
            str(month) + ' ' +
            str(day) + ' ' +
            str(hour) + ':' +
            str(minute), "%Y %m %d %H:%M")

    def __cmp__(self, other):
        data = 0
        if (self.date > other.date):
            data = 1
        elif (self.date < other.date):
            data = -1
        return data

class NewsItemListHelper:
    ''' # TODO: Refactor this out of here. '''

    newspageNames = list()

    def addNewspageName(self, pageName):
        self.newspageNames += [pageName]

    def getNewspageNames(self):
        return self.newspageNames

    def getRecentArticles(self, daysOld, numberOfArticles):
        ''' Get a list of BriefArticles for the most recently edited articles.
            Returns an empty list if there are no recent articles.

            daysOld - maximum age of articles to retrieve in days
            numberOfArticles - maximum number of articles to retrieve
        '''
        data = list()
        adao = ArticleDaoFactory.create()
        try:
            for newspageName in self.newspageNames:
                articles = adao.fetchSorted(newspageName=newspageName, sortType=SORT_DATE_LM, limit=numberOfArticles)

                for article in articles:
                    if (article.isOld(daysOld, False)):
                        pass # TODO: change this to break when you know sorting is working correctly
                    else:
                        ba = BriefArticle()
                        ba.newspage = newspageName
                        ba.uid = article.id
                        ba.title = article.title
                        ba.prettyDate = article.getSimpleDateString()
                        if (article.modifiedDate is not None):
                            ba.prettyModifiedDate = article.getSimpleDateString(False)
                            ba.setDate(
                                article.modifiedDate.timetuple()[0],
                                article.modifiedDate.timetuple()[1],
                                article.modifiedDate.timetuple()[2],
                                article.modifiedDate.timetuple()[3],
                                article.modifiedDate.timetuple()[4])
                        else:
                            ba.prettyModifiedDate = article.getSimpleDateString()
                            # I need to do this for legacy data
                            ba.setDate(
                                article.createdDate.timetuple()[0],
                                article.createdDate.timetuple()[1],
                                article.createdDate.timetuple()[2],
                                article.createdDate.timetuple()[3],
                                article.createdDate.timetuple()[4])
                        data += [ba]
        finally:
            adao.cleanUp()

        data.sort()
        data.reverse()
        if (len(data) > numberOfArticles):
            data = data[0:numberOfArticles]

        return data