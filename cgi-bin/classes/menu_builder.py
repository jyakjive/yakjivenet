# imports
from newscommunity.application import APPLICATION
#from article import *
from article_handler import *
from article_utils import *
from section_handler import *
from newspage_handler import *
from db.article_dao import *

# declarations

# definitions

# classes

class MenuBuilder:
    ''' The MenuBuilder needs to
        Get all the sections that have published newspages with published articles
        Get all the visible info pages
        Expose a method to retrieve the menu, passing in the current section/info page

    '''

    def __init__(self, sections = None, newspages = None, infoPages = None):
        self.sections = sections
        self.newspages = newspages
        self.infoPages = infoPages
        self.menuHasInfoPages = True

        self.articleCountDict = dict()
        self.sectionPageDict = dict()
        self.newspageNavDict = dict()
        self.pageDictBuilt = False
        self._buildPageDict_()

    def _hasVisibleArticles_(self, newspageName):
        data = 0
        if (newspageName in self.articleCountDict):
            data = self.articleCountDict[newspageName]
        return data

    def _buildArticleNavList_(self):
        ''' Return a collection of page names for segmented newspages.  If the
            newspage is sorted by date, return a list.  If it's sorted otherwise,
            return a dict.
        '''
        if (self.newspages is None):
            raise 'Newspages is none in MenuBuilder'

        adao = ArticleDaoFactory.create()

        try:
            #Create the list of month-year combos for the picklist
            for newspage in self.newspages:
                if (self.sections[self.newspages[newspage].newspage].isVisible and self.newspages[newspage].isVisible):
                    articles = adao.fetchSorted(newspage, self.newspages[newspage].sortType, publishedOnly=True)
                    if (len(articles) == 0):
                        continue

                    # TODO: See if this is even necessary... gVI doesn't do what I think here
                    self.articleCountDict[newspage] = len(articles)

                    pageList = list()
                    page = self.newspages[newspage]
                    if (page.pageType == PAGE_LONG_ARTICLES):
                        for item in articles:
                            if (item.published):
                                articleName = getArticlePageName(page, articles, item) # get the URL for the article
                                articleName = articleName.split('/') # create a list of tokens
                                articleName = articleName[len(articleName) - 1] # get only the 'filename.html'
                                articleName = articleName[0:len(articleName) - 5] # trim the '.html'
                                pageList.append(articleName)
                    elif (page.sortType in [SORT_DATE, SORT_DATE_REVERSE]):
                        lastMonth = int(articles[0].publishedDate.timetuple()[1])
                        lastYear = int(articles[0].publishedDate.timetuple()[0])
                        for item in articles:
                            itemMonth = int(articles[0].publishedDate.timetuple()[1])
                            itemYear = int(articles[0].publishedDate.timetuple()[0])
                            if ((itemYear != lastYear) or (itemMonth != lastMonth)):
                                itemMonth = int(item.month)
                                itemYear = int(item.year)
                                pageList.append(str(itemMonth) + '-' + (str(itemYear)[2:]))
                            lastMonth = itemMonth
                            lastYear = itemYear
                    else:
                        count = 0
                        first = ''
                        last = ''
                        for item in articles:
                            if ((count % ITEMS_PER_PAGE) == 0):
                                last = item.title[0:4]
                                if (count > 0):
                                    pageList.append(str(first) + ' to ' + str(last))
                                first = item.title[0:4]
                            count += 1
                        if ((count % ITEMS_PER_PAGE) > 0):
                            last = articles[count - 1].title[0:4]
                            pageList.append(str(first) + ' to ' + str(last))

                    if (len(pageList) > 0):
                        self.newspageNavDict[newspage] = pageList
        finally:
            adao.cleanUp()

    def _buildPageDict_(self):
        ''' Build a dictionary that looks like:
            {sectionName1:[newspage1,newspage2], sectionName2:[newspage4,newspage3]}
        '''
        if (not self.pageDictBuilt):
            if (self.sections is not None):
                self._buildArticleNavList_()
                rankDict = getRankDict(self.newspages)
                rankKeys = rankDict.keys()
                rankKeys.sort()

                sectionList = buildSectionList(self.sections)

                temp = 0

                homepageSection = getHomepageSection(self.sections)
                for section in sectionList:
                    pagelist = list()
                    if (section.isVisible):
                        for rKey in rankKeys:
                            page = rankDict[rKey]
                            if (self.newspages[page].newspage == section.name):
                                if ((self.newspages[page].isVisible == True) and (self._hasVisibleArticles_(page))):
                                    pagelist += [page]
                        if (len(pagelist) > 0):
                            self.sectionPageDict[section.name] = pagelist


            self.pageDictBuilt = True

    def _getSectionMenu_(self, currentSection = None):
        data = ''
        if (self.sections is not None):
            sectionList = buildSectionList(self.sections)
            homepageSection = getHomepageSection(self.sections)
            for section in sectionList:
                if (section.isVisible and (section.name in self.sectionPageDict)):
                    data += '<li>'
                    #if ((data != '') and (APPLICATION.menuSeparator != '')):
                    #    data += APPLICATION.menuSeparator

                    if (section.name != homepageSection):
                        if (section.name != currentSection):
                            data += '<a href="' + APPLICATION.rootURL + section.name + '.html" title="Go to the ' + section.longname + ' section">'
                        else:
                            data += '<a href="' + APPLICATION.rootURL + section.name + '.html" title="Go to the ' + section.longname + ' section" class="selectedSectionMenu">'
                        data += section.longname
                        data += '</a>'
                    else:
                        if (section.name != currentSection):
                            data += '<a href="' + APPLICATION.rootURL + 'index.html" title="Go to the main page section">'
                        else:
                            data += '<a href="' + APPLICATION.rootURL + 'index.html" class="selectedSectionMenu">'
                        data += 'Home'
                        data += '</a>'
                    data += '</li>\n'
        return data

    def _getInfoPageMenu_(self, currentInfoPage = None):
        data = ''
        if (self.infoPages is not None):
            for page in self.infoPages:
                if (page.isVisible and (page.name != INFO_PAGE_CONTACT_THANKS)):
                    if ((page.name == INFO_PAGE_CONTACT) and (APPLICATION.contactEmail == '')):
                        continue
                    data += '<li>'
                    #if ((data != '') and (APPLICATION.menuSeparator != '')):
                    #    data += APPLICATION.menuSeparator
                    if (currentInfoPage != page.name):
                        data += '<a href="' + APPLICATION.rootURL + page.filename + '" title="Go to the ' + page.title + ' page">'
                    else:
                        data += '<a href="' + APPLICATION.rootURL + page.filename + '" title="Go to the ' + page.title + ' page" class="selectedSectionMenu">'
                    data += page.menuName
                    data += '</a>'
                    data += '</li>\n'
        return data

    def _getNewspageMenu_(self, currentSection = None, currentNewspage = None):
        data = ''
        if (currentSection is not None):
            if ((self.sections is not None) and (currentSection in self.sectionPageDict)):
                section = self.sections[currentSection]
                for pageName in self.newspages:
                    if ((currentSection in self.sectionPageDict) and (pageName in self.sectionPageDict[currentSection])):
                        data += '<li>'
                        page = self.newspages[pageName]
                        pageURL = pageName
                        if (page.pageType == PAGE_LONG_ARTICLES):
                            pageURL = self.newspageNavDict[pageName][0]
                        if (pageName != currentNewspage):
                            data += '<a href="' + APPLICATION.rootURL + pageURL + '.html" title="Go to the ' + page.title + ' newspage">'
                        else:
                            data += '<a href="' + APPLICATION.rootURL + pageURL + '.html" class="selectedNewspageMenu">'
                        data += page.title
                        data += '</a></li>\n'
        return data

    def _getArticleNav_(self, currentNewspage, currentArticlePage = None):
        data = ''
        if (currentNewspage is not None):
            if ((currentNewspage is not None) and (currentNewspage in self.newspageNavDict)):
                if (self.newspages[currentNewspage].pageType == PAGE_LONG_ARTICLES):
                    data = self._getArticleNavigationByLongArticle_(currentNewspage, currentArticlePage)
                elif (self.newspages[currentNewspage].sortType in [SORT_DATE, SORT_DATE_REVERSE]):
                    data = self._getArticleNavigationByDate_(currentNewspage, currentArticlePage)
                else:
                    data = self._getArticleNavigationByCount_(currentNewspage, currentArticlePage)
        return data

    def _getArticleNavigationByLongArticle_(self, currentNewspage, currentArticlePage):
        ''' Get the navigation for long articles.  I'd like it to be:
                First
                Previous
                Next
                Last
        '''
        # currentArticlePage looks like 'page-name-1' where 1 is the uid of an article

        data = ''

        adao = ArticleDaoFactory.create()
        try:
            articles = adao.fetchSorted(currentNewspage, self.newspages[currentNewspage].sortType, publishedOnly = True)

            if (len(articles) > 0):
                pageList = self.newspageNavDict[currentNewspage]
                if (len(pageList) > 0):
                    for i in range(len(pageList)):
                        uid = pageList[i].split('-')
                        uid = int(uid[len(uid)-1])

                        article = adao.fetchByID(uid)

                        selClazz = None

                        if (pageList[i] == currentArticlePage):
                            selClazz = 'selectedArticleMenu'
                        data += '<li>' + createLink(APPLICATION.rootURL + pageList[i] + '.html', article.title, article.title, clazz=selClazz) + '</li>\n'
        finally:
            adao.cleanUp()

        return data

    def _getArticleNavigationByLongArticle2_(self, currentNewspage, currentArticlePage):
        ''' DEPRECATED: Get the navigation for long articles.  I'd like it to be:
                First
                Previous
                Next
                Last
        '''
        # currentArticlePage looks like 'page-name-1' where 1 is the uid of an article

        data = ''
        pageList = self.newspageNavDict[currentNewspage]
        if (len(pageList) > 0):
            for i in range(len(pageList)):
                # create the FIRST item
                if ((i == 0) and (currentArticlePage != pageList[i])):
                    data += '<li>' + createLink(APPLICATION.rootURL + pageList[i] + '.html', 'First article', 'first article') + '</li>\n'

                if (len(pageList) > 2):
                    # create the PREVIOUS item
                    if ((i > 1) and (currentArticlePage == pageList[i])):
                        data += '<li>' + createLink(APPLICATION.rootURL + pageList[i-1] + '.html', 'Previous article', 'previous article') + '</li>\n'

                    # create the NEXT item
                    if ((i < (len(pageList) - 2)) and (currentArticlePage == pageList[i])):
                        data += '<li>' + createLink(APPLICATION.rootURL + pageList[i+1] + '.html', 'Next article', 'next article') + '</li>\n'

                # create the LAST item
                if ((i == (len(pageList) - 1)) and (currentArticlePage != pageList[i])):
                    data += '<li>' + createLink(APPLICATION.rootURL + pageList[i] + '.html', 'Last article', 'last article') + '</li>\n'
        return data

    def _getArticleNavigationByCount_(self, currentNewspage, currentArticlePage):
        data = ''
        pageList = self.newspageNavDict[currentNewspage]
        if (len(pageList) > 0):
            for i in range(len(pageList)):
                ii = ''
                if (i > 0):
                    ii = str(i)
                data += '<li>'
                #if ((currentArticlePage is not None) and (currentNewspage is not None)):
                #    raise '[' + str(currentArticlePage) + ':' + str(currentNewspage) + ']'
                if (currentArticlePage == (currentNewspage + ii)):
                    data += '<a href="' + APPLICATION.rootURL + currentNewspage + ii + '.html' + \
                        '" title="Articles from ' + pageList[i] + '" class="selectedArticleMenu">' + pageList[i]
                else:
                    data += '<a href="' + APPLICATION.rootURL + currentNewspage + ii + '.html' + \
                        '" title="Articles from ' + pageList[i] + '">' + pageList[i]
                data += '</a></li>\n'
        return data

    def _getArticleNavigationByDate_(self, currentNewspage, currentArticlePage):
        data = ''
        pageList = self.newspageNavDict[currentNewspage]
        if (len(pageList) > 0):
            data += '<li>'
            styleText = ' class="selectedArticleMenu"'

            insertText = ''
            if (currentArticlePage == currentNewspage):
                insertText = styleText
            if (self.newspages[currentNewspage].sortType == SORT_DATE):
                data += '<a href="' + APPLICATION.rootURL + currentNewspage + \
                    '.html" title="Articles for current month"' + insertText + '>recent'
            else:
                data += '<a href="' + APPLICATION.rootURL + currentNewspage + \
                    '.html" title="Articles for the first month"' + insertText + '>oldest'
            data += '</a></li>\n'

            for item in pageList:
                data += '<li>'
                if (str(currentNewspage + item) == str(currentArticlePage)):
                    data += '<a href="' + APPLICATION.rootURL + currentNewspage + item + '.html' + \
                        '" title="News items for ' + item + '"' + styleText + '>' + item
                else:
                    data += '<a href="' + APPLICATION.rootURL + currentNewspage + item + '.html' + \
                        '" title="News items for ' + item + '">' + item
                data += '</a></li>\n'
        return data

    def getSectionMenu(self, currentSection = None):
        data = self.wrapSectionList(self._getSectionMenu_(currentSection))
        return data

    def getInfoPageMenu(self, currentInfoPage = None):
        data = self.wrapSectionList(self._getInfoPageMenu_(currentInfoPage))
        return data

    def wrapSectionList(self, data):
        if (data <> ''):
            data = '<div id="sectionMenuDiv">\n<ul>\n' + data + '</ul>\n</div>\n'
        return data

    def wrapNewspageList(self, data):
        if (data <> ''):
            data = '<div id="newspageMenuDiv">\n<ul>\n' + data + '</ul>\n</div>\n'
        return data

    def wrapArticleList(self, data):
        if (data <> ''):
            data = '<div id="articleMenuDiv">\n<ul>\n' + data + '</ul>\n</div>\n'
        return data

    def wrapAnchor(self, data):
        if (data <> ''):
            data = '<a>\n' + data + '</a>\n'
        return data

    def getMenu(self, currentSection = None, currentInfoPage = None, currentNewspage = None, currentArticlePage = None):
        ''' The menu could be called from a Section, from an InfoPage, or from a Newspage.
            It should have different behavior in all cases.
        '''
        # Get the current section if we were to deep to figure that out from the newspage context
        if ((currentSection is None) and (currentNewspage is not None)):
            for section in self.sectionPageDict:
                if (currentNewspage in self.sectionPageDict[section]):
                    currentSection = section
                    break

        data = ''
        if ((self.sections is not None) and (self.newspages is not None)):
            data += self._getSectionMenu_(currentSection)
        if (self.infoPages is not None):
            data += self._getInfoPageMenu_(currentInfoPage)
        data = self.wrapSectionList(data)

        data2 = ''
        if ((self.sections is not None) and (self.newspages is not None)):
            # newspage nav
            data2 += self._getNewspageMenu_(currentSection, currentNewspage)
            data2 = self.wrapNewspageList(data2)
            data += data2

            # article nav
            data2 = self._getArticleNav_(currentNewspage, currentArticlePage)
            data2 = self.wrapArticleList(data2)
            data += data2
        return data

    def setMenuHasInfoPages(self, flag = True):
        self.menuHasInfoPages = flag
