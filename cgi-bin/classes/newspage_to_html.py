#imports
#from article import *
from newscommunity.application import APPLICATION
from newscommunity.templatevars import *
from newscommunity.ncvars import *
from article_to_html import *
from article_utils import *
from util.fileutils import Semaphore, writeTextFile
from db.article_dao import *
from article import generateRSSName

#declarations
semname = 'newsPageSem'

#definitions

def getSubTitle(page):
    data = page.subTitle
    if (APPLICATION.subTitleDate):
        if ((data is not None) and (data != '')):
            data += ' - '
        data += getTodayHTML()
    return data

#classes
class NewsPageMaker:

    def __init__(self, theNewspage = 'Has not been set', imageUrl = None, menuBuilder = None):
        """Initialze the class with a file name relative to the path of the root script.
            filename - the location + name of the news items file
        """
        self.title = '${pageTitle}'
        self.subTitle = '${subTitle}'
        self.heading = '${pageHeading}'
        self.newsHTML = '${divBox3}'
        self.newsTOC = '${simpleTOC}'
        self.rssurl = '${rssurl}'
        self.divInsert = '${divInsert}'
        self.newsletter = '${newsletter}'
        self.newspageName = '${newspageName}'

        self.menuBuilder = menuBuilder

        self.theNewspage = theNewspage
        self.articles = None

    def toHTML(self, templatename, page, fileDir, rssurl, addNewsletter = False, sectionMenu = ''):
        """Process the page.

            templatename - the location + name of the page template file
            page - the page object to be generated into HTML
            fileDir - the directory where pages are to be written
        """

        if (self.articles is None):
            adao = ArticleDaoFactory.create()
            try:
                self.articles = adao.fetchSorted(self.theNewspage, page.sortType)

                if (len(self.articles) == 0):
                    return
            finally:
                adao.cleanUp()

        #Read in the template file
        pageTemplate = ''
        try:
            f = file(templatename)
            pageTemplate = f.read()
            f.close()

            replaceDict = dict()
            replaceDict['domain'] = APPLICATION.domainName
            replaceDict['siteTitle'] = APPLICATION.siteTitle
            replaceDict['metaKeywords'] = APPLICATION.metaKeywords
            replaceDict['metaDescription'] = APPLICATION.metaDescription
            if (APPLICATION.customStyle):
                replaceDict['style'] = APPLICATION.rootURL + APPLICATION.styleName
            else:
                replaceDict['style'] = APPLICATION.styleURL + APPLICATION.styleName
            replaceDict['printStyleURL'] = APPLICATION.printStyleURL
            replaceDict['divUser1'] = ''
            replaceDict['divUser2'] = ''
            replaceDict['divUser3'] = ''
            replaceDict['divUser4'] = ''
            #replaceDict[''] = APPLICATION.

            for item in replaceDict:
                pageTemplate = pageTemplate.replace('${' + item + '}', replaceDict[item])
        except IOError:
            raise "IOError attempting to access:", templatename

        if (page.pageType == PAGE_LONG_ARTICLES):
            count = 0
            for i in range(len(self.articles)):
                # Each article get's a page

                # Get the full page name # WORKING
                articleURL = getArticlePageName(page, self.articles, self.articles[i])

                # Parse out the file name
                newPageName = articleURL.split('/')
                newPageName = newPageName[len(newPageName) - 1]

                # Start creating the page
                newPage = pageTemplate
                newPage = newPage.replace(self.newspageName, page.name)
                newPage = newPage.replace(self.title, page.title)
                newPage = newPage.replace(self.heading, page.title)
                newPage = newPage.replace(self.subTitle, getSubTitle(page))
                newPage = newPage.replace(self.newsHTML, \
                    itemListToHTML(self.articles, page, \
                    startCount = i, endCount = (i + 1)))
                newPage = newPage.replace(self.newsTOC,
                    itemListToSimpleTOCList(
                    rssURL = generateRSSName(APPLICATION.siteID, page.name, APPLICATION.rssFullURL),
                    adOnly = True))
                newPage = newPage.replace(self.rssurl, rssurl)
                diText = ''
                if ((page.allowComments) or (page.isBlog)):
                    diText += DIV_COMMENTS
                newPage = newPage.replace(self.divInsert, diText)
                if (addNewsletter):
                    nltext = self.__getNewsletterText__()
                    newPage = newPage.replace(self.newsletter, nltext)
                else:
                    newPage = newPage.replace(self.newsletter, '')

                if (self.menuBuilder is None):
                    newPage = newPage.replace('${sectionMenu}', sectionMenu)
                else:
                    newPage = newPage.replace(
                            '${sectionMenu}', self.menuBuilder.getMenu(currentNewspage=page.name,
                            currentArticlePage=(newPageName[0:len(newPageName) - 5])))

                newPage = newPage.replace('${adminURL}', APPLICATION.adminURL)
                self.__writePage__(fileDir + newPageName, newPage)
        elif (page.sortType in [SORT_DATE, SORT_DATE_REVERSE]):

            #Loop through the possible pages
            recentMonth = int(self.articles[0].publishedDate.timetuple()[1])
            recentYear = int(self.articles[0].publishedDate.timetuple()[0])
            oldestMonth = int(self.articles[len(self.articles) - 1].publishedDate.timetuple()[1])
            oldestYear = int(self.articles[len(self.articles) - 1].publishedDate.timetuple()[0])

            lastMonth = 0
            lastYear = 0
            # This is looping through all the date-sorted news items to find one from each
            # month, then generating the news page for that month.
            # TODO-L: refactor
            for item in self.articles:
                itemMonth = int(item.publishedDate.timetuple()[1])
                itemYear = int(item.publishedDate.timetuple()[0])
                if ((itemMonth != lastMonth) | (itemYear != lastYear)):
                    newPage = pageTemplate
                    if ((itemMonth == recentMonth) & (itemYear == recentYear)):
                        newPageName = page.name + '.html'
                    else:
                        # TODO-L: Consider offering the ability to slice out the millenium and century as an optional param
                        newPageName = page.name + (str(itemMonth) + '-' + (str(itemYear)[2:]) + '.html')
                    newPage = newPage.replace(self.title, page.title)
                    newPage = newPage.replace(self.heading, page.title)
                    newPage = newPage.replace(self.subTitle, getSubTitle(page))
                    newPage = newPage.replace(self.newsHTML, \
                        itemListToHTML(self.articles, page, itemYear, itemMonth))
                    if (page.pageType != PAGE_LINKS):
                        newPage = newPage.replace(self.newsTOC, \
                            itemListToSimpleTOCList(self.articles, newPageName, itemYear, itemMonth,
                            rssURL = generateRSSName(APPLICATION.siteID, page.name, APPLICATION.rssFullURL)))
                    else:
                        newPage = newPage.replace(self.newsTOC, '')
                    newPage = newPage.replace(self.rssurl, rssurl)
                    diText = ''
                    if ((page.allowComments) or (page.pageType == PAGE_BLOG) or (page.isBlog)):
                        diText += DIV_COMMENTS
                    if (page.pageType == PAGE_GUESTBOOK):
                        diText += DIV_GUESTBOOK
                    newPage = newPage.replace(self.divInsert, diText)
                    if (addNewsletter):
                        nltext = self.__getNewsletterText__()
                        newPage = newPage.replace(self.newsletter, nltext)
                    else:
                        newPage = newPage.replace(self.newsletter, '')

                    if (self.menuBuilder is None):
                        newPage = newPage.replace('${sectionMenu}', sectionMenu)
                    else:
                        newPage = newPage.replace(
                                '${sectionMenu}', self.menuBuilder.getMenu(currentNewspage=page.name,
                                currentArticlePage=(newPageName[0:len(newPageName) - 5])))

                    newPage = newPage.replace('${adminURL}', APPLICATION.adminURL)

                    self.__writePage__(fileDir + newPageName, newPage)
                lastMonth = itemMonth
                lastYear = itemYear
        else:
            count = 0
            for i in range(len(self.articles)):
                if ((i % ITEMS_PER_PAGE) == 0):
                    newPage = pageTemplate
                    if (count == 0):
                        newPageName = page.name + '.html'
                    else:
                        newPageName = page.name + str(count) + '.html'
                    newPage = newPage.replace(self.title, page.title)
                    newPage = newPage.replace(self.heading, page.title)
                    newPage = newPage.replace(self.subTitle, getSubTitle(page))
                    newPage = newPage.replace(self.newsHTML, \
                        itemListToHTML(self.articles, page, \
                        startCount = i, endCount = (i + ITEMS_PER_PAGE)))
                    if (page.pageType != PAGE_LINKS):
                        newPage = newPage.replace(self.newsTOC,
                            itemListToSimpleTOCList(self.articles, newPageName,
                            startCount = i, endCount = (i + ITEMS_PER_PAGE),
                            rssURL = generateRSSName(APPLICATION.siteID, page.name, APPLICATION.rssFullURL)))
                    else:
                        newPage = newPage.replace(self.newsTOC, '')
                    #newPage = newPage.replace(self.pageNav, self.__genPageNavigationByCount__(pageList, page.name))
                    newPage = newPage.replace(self.rssurl, rssurl)
                    diText = ''
                    if ((page.allowComments) or (page.pageType == PAGE_BLOG) or (page.isBlog)):
                        diText += DIV_COMMENTS
                    if (page.pageType == PAGE_GUESTBOOK):
                        diText += DIV_GUESTBOOK
                    newPage = newPage.replace(self.divInsert, diText)
                    if (addNewsletter):
                        nltext = self.__getNewsletterText__()
                        newPage = newPage.replace(self.newsletter, nltext)
                    else:
                        newPage = newPage.replace(self.newsletter, '')

                    if (self.menuBuilder is None):
                        newPage = newPage.replace('${sectionMenu}', sectionMenu)
                    else:
                        newPage = newPage.replace(
                                '${sectionMenu}', self.menuBuilder.getMenu(currentNewspage=page.name,
                                currentArticlePage=(newPageName[0:len(newPageName) - 5])))

                    newPage = newPage.replace('${adminURL}', APPLICATION.adminURL)
                    self.__writePage__(fileDir + newPageName, newPage)
                    count += 1


        # Write the RSS files here, too
        rssData = itemListToRSSXML(self.articles, str(APPLICATION.rootURL + page.name + '.html'))
        rssFileName = APPLICATION.rssDirectory + APPLICATION.siteID + '-' + page.name + '-rss.xml'
        writeTextFile(rssFileName, rssData)

    def __getNewsletterText__(self):

        nlbody = 'Please enter your name:\n'
        nlbody += createTextInput('nl_name') + '<BR>\n'
        nlbody += 'Please enter your email:\n'
        nlbody += createTextInput('nl_email') + '\n'
        nlbody += '<BR>\n'
        nlbody += '<INPUT TYPE=BUTTON NAME=SUBMIT VALUE="Submit" onMousedown="javascript:validateNLForm()">'
        nlbody = createForm('nlform', APPLICATION.adminURL + 'submit_newsletter_recipient.py', \
            'POST', nlbody, target = 'nltarget') + '\n'

        nlscript = '<SCRIPT TYPE="text/javascript">\n'
        nlscript += 'function validateNLForm(){\n'
        nlscript += '    if (!checkValidEmail(getFromForm("nl_email", "nlform").value)){\n'
        nlscript += '        alert("Please enter a valid email.");\n'
        nlscript += '    } else {\n'
        nlscript += '        getForm("nlform").submit();\n'
        nlscript += '    }\n'
        nlscript += '}\n'
        nlscript += '</SCRIPT>\n'

        nlbody = nlscript + nlbody
        nlbody += '<IFRAME NAME="nltarget" HEIGHT="0" WIDTH="0"></IFRAME>\n'
        #nltext = createFloatingDiv('Sign up for newsletter', \
        #    'Sign up for newsletter', nlbody, 'newsletter', False, \
        #    'newsletter', yshift = -200)
        nltext = createPopupLink('Sign up for our newsletter', 'Sign up for our newsletter',
            nlbody, clazz='guestbook', divID='newsletter')
        return nltext

    def __writePage__(self, filename, pageData):
        #Write the page to a file

        try:
            sem = Semaphore(semname)
            sem.put()

            ff = file(filename, 'w')
            ff.write(str(pageData))
            ff.flush()
            ff.close()

            sem.remove()
        except IOError:
            raise "IOError attempting to write:", filename
