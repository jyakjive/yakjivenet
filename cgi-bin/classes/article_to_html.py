
# imports
from newscommunity.ncvars import *
from util.image_utils import *
from util.html_utils import *
from time import * # TODO: Check to see if I need this line
from util.user_management import *
from util.utils import remember
from util.fileutils import Semaphore
from newscommunity.application import APPLICATION
from ui.stripper import Stripper
from util.text_utils import *
from ui.ad_inserter import *
import random
from db.article_dao import *
import datetime
from article import RSSTemplate

'''This package is designed to hold some static methods that will be used to
generate HTML and XML from the NewsItem and NewsItemList classes.'''

# Definitions

def getUserParser():
    data = remember('userParser')
    if (data is None):
        data = UserDataParser(FILENAME_USERS)
        remember('userParser', data)
    return data

def safeRSSText(data):
    '''I need to strip out all HTML for RSS files and other XML files in some cases.'''
    # TODO: Strip out all HTML from RSS and other XML files.
    try:
        data = str(data)
        stripper = Stripper()
        data = stripper.strip(data)
    except:
        strData = ''
        for i in range(len(data)):
            if (ord(data[i]) > 128):
                strData += ' '
            else:
                strData += data[i]
        data = strData
    return data

def getDateAsInt(day, month, year):
    dateInt = 0
    if ((year != '') and (month != '') and (day != '')):
        dateInt = int(year) * 10000
        dateInt += (int(month) * 100)
        dateInt += int(day)
    return dateInt

def getStartHTML(dateString = None):
    '''Open the HTML for an item list HTML block.'''
    data = ''
    #if (dateString is not None):
    #    data += '    <H1>' + dateString + '</H1>\n'
    return str(data)

def getEndHTML():
    '''Close the HTML for an item list HTML block.'''
    data = ''
    return str(data)

def itemListToHTML(articles, page, \
        year = None, month = None, \
        startCount = None, endCount = None):
    """Get the HTML for news items.
        year - YYYY
        month - MM
    """
    data = None
    if (len(articles) > 0):
        # TODO: make sure to get them sorted
        data = ''
        lastDate = 0
        if (startCount == None):
            for i in range(len(articles)):
                item = articles[i]
                if (not item.published):
                    continue
                inDate = (year == None) or (month == None) or ((int(year) == int(item.publishedDate.timetuple()[0])) and
                        (int(month) == int(item.publishedDate.timetuple()[1])))
                if (inDate):
                    if ((page.pageType == '') or
                            (page.pageType == PAGE_HEADLINES) or
                            (page.pageType == PAGE_BLOG) or
                            (page.pageType == PAGE_GUESTBOOK) or
                            (page.pageType == PAGE_LONG_ARTICLES) or
                            (page.pageType == PAGE_LETTERS)):
                        if ((i == 0) or (item.getDateAsInt() <> lastDate)):
                            # REFACTOR: I don't think this date is even used in here
                            data += getStartHTML(item.getSimpleDateString())
                        data += itemToListHTML(item, page)
                        if (i < (len(articles) - 1)):
                            nextItem = articles[i + 1]
                        if ((i == (len(articles) - 1)) or \
                               ((i < (len(articles) - 1)) and \
                               (item.getDateAsInt() <> nextItem.getDateAsInt()))):
                            data+= getEndHTML();
                        lastDate = item.getDateAsInt()
                    elif (page.pageType == PAGE_LINKS):
                        data += itemToLinkHTML(item)
                    elif (page.pageType == PAGE_PHOTOS):
                        pass
                    else:
                        # don't have anything else at the moment
                        pass
        else:
            count = 0
            for i in range(len(articles)):
                item = articles[i]
                if (not item.published):
                    continue
                if ((count >= startCount) and (count < endCount)):
                    if ((page.pageType == '') or
                            (page.pageType == PAGE_HEADLINES) or
                            (page.pageType == PAGE_BLOG) or
                            (page.pageType == PAGE_GUESTBOOK) or
                            (page.pageType == PAGE_LONG_ARTICLES) or
                            (page.pageType == PAGE_LETTERS)):
                        if (count == startCount):
                            data += getStartHTML()
                        data += itemToListHTML(item, page, showDate = True)
                        if (i < (len(articles) - 1)):
                            nextItem = articles[i + 1]
                        if ((i == (len(articles) - 1)) or \
                               (count == endCount)):
                            data+= getEndHTML();
                    elif (page.pageType == PAGE_LINKS):
                        data += itemToLinkHTML(item)
                    elif (page.pageType == PAGE_PHOTOS):
                        pass
                    else:
                        # don't have anything else at the moment
                        pass
                count += 1
    return data

def itemListToSimpleTOCList(articles = None, pageName = None, year = None, month = None, \
        startCount = None, endCount = None, rssURL = None, adOnly = False):
    """Converts the news item titles to a simple list for representation in a web page as a TOC for the given category.
    This will need to be modified if/when I implement the pagination mechanism... hopefully with some kind of date-based
    page identifier.

        pageName - the base url of the page where the items can be seen
        year - YYYY
        month - MM
    """

    data = '<div id="simpleTOC">'
    if (rssURL is not None):
        data += createLink(rssURL,
            'See the RSS 2.0 feed for this page', '<span class="itemTitle">RSS 2.0</span>') + '<br>&nbsp;<br>\n'

    if (not adOnly):
        if ((articles is None) or (pageName is None)):
            raise Exception('Item list and pageName cannot be none for non-ad-only TOC\'s.')

        if (len(articles) > 0):
            data += '<span class="itemTitle">Page contents</span>\n<ul>\n'
            if (startCount is None):
                for item in articles:
                    if (item.published):
                        if ((year == None) or (month == None)):
                            data += '<li><a href="' + pageName + '#' + str(item.id) + \
                                '" title="' + safeText(item.title) + '">' + safeText(item.title) + '</a>\n'
                        else:
                            if ((int(year) == int(item.publishedDate.timetuple()[0])) and (int(month) == int(item.publishedDate.timetuple()[1]))):
                                data += '<li><a href="' + pageName + '#' + str(item.id) + \
                                    '" title="' + safeText(item.title) + '">' + safeText(item.title) + '</a>\n'
            else:
                count = 0
                for i in range(len(articles)):
                    item = articles[i]
                    if (not item.published):
                        continue
                    if ((count >= startCount) and (count < endCount)):
                        data += '<li><a href="' + pageName + '#' + str(item.id) + \
                            '" title="' + safeText(item.title) + '">' + safeText(item.title) + '</a>\n'
                    count += 1
            data += '</ul>\n'

    if (APPLICATION.showAds):
        data += '<br/>&nbsp;<br/>\n'
        data += generateVerticalBannerAd()

    data += '</div>\n'

    return str(data)

def itemListToRSSXML(articles, pageURL, year = None, month = None):
    """Get the RSS XML for a news page.
        year - YYYY
        month - MM
    """
    data = None
    if (len(articles) > 0):
        data = ''
        count = 0
        for item in articles:
            if (item.published):
                count += 1
                if (((year == None) or (month == None)) or
                        ((int(year) == int(item.publishedDate.timetuple()[0])) and
                        (int(month) == int(item.publishedDate.timetuple()[1])))):
                    data += itemToRSSXML(item, pageURL)
                if (count == 5):
                    break
    rsstemp = RSSTemplate(FILENAME_RSS)
    data = rsstemp.getHeader() + str(data)
    data = data + rsstemp.getFooter()
    return data

#from NewsItem

def itemToRSSXML(article, page):
    xml = '  <item>\n'
    xml += '    <title>' + safeText(article.title)  + '</title>\n'
    xml += '    <link>' + page + '#' + str(article.id) + '</link>\n'
    content = article.content
    if ((content is None) or (content == '')):
        content = article.title
    lendesc = 150
    desc = safeRSSText(content)[0:lendesc]
    while (desc.count('<') > desc.count('>')):
        lendesc += 1
        desc = safeRSSText(content[0:lendesc])
    xml += '    <description>' + desc + '...</description>\n'
    xml += '    <pubDate>' + article.getXMLDateString() + '</pubDate>\n'
    xml += '    <guid>' + page + '#' + str(article.id) + '</guid>\n'
    xml += '    <category>US ' + safeText(article.category) + '</category>\n'
    xml += '  </item>\n'

    return str(xml)

def getAuthorHTML(article):
    data = ''
    if (article.createdBy != NC_ADMIN):
        userParser = getUserParser()
        data = '<br><span class="postedBy">posted by '
        user = userParser.getUser(article.createdBy)
        if ((user is not None) and not user.privateProfile):
            data += createLink(href=(APPLICATION.adminURL + 'show_contributor.py?nickname=' + article.createdBy), \
                text=article.createdBy, target='authorWin')
        else:
            if (article.createdBy != NC_GUEST):
                data += article.createdBy
            else:
                data += article.sourceName
        data += '</span>\n'
    return data

def getAddressHTML(article):
    data = ''
    if ((article.street not in [None, '']) or
            (article.street2 not in [None, '']) or
            (article.city not in [None, '']) or
            (article.state not in [None, '']) or
            (article.zip not in [None, '']) or
            (article.country not in [None, '']) or
            (article.phone not in [None, ''])):
        data = '<div class="addressTitle">Address:</div>\n<div class="addressInfo">'
        if ((article.street is not None) and (article.street != '')):
            data += ' ' + article.street
        if ((article.street2 is not None) and (article.street2 != '')):
            data += '<br>' + article.street2
        data += '<br>'
        if ((article.city is not None) and (article.city != '')):
            data += ' ' + article.city
        if ((article.state is not None) and (article.state != '')):
            if ((article.city is not None) and (article.city != '')):
                data += ','
            data += ' ' + article.state
        if ((article.zip is not None) and (article.zip != '')):
            data += ' ' + article.zip
        if ((article.country is not None) and (article.country != '')):
            data += ' ' + article.country
        if ((article.country is not None) and (article.country != '')):
            data += '<br>Phone: ' + article.phone
        data += '</div>\n'
    return data

def getCoordinateHTML(article):
    data = ''
    if (((article.longitude not in [None, '']) and (article.latitude not in [None, ''])) or
            (article.altitude not in [None, ''])):
        data = '<div class="coordinatesTitle">Coordinates:</div>\n'
    if ((article.longitude not in [None, '']) and (article.latitude not in [None, ''])):
        data += '<div class="coordinatesInfo">'
        data += 'Longitude: ' + repr(article.longitude)
        data += '<br>Latitude: ' + repr(article.latitude)
    if (article.altitude not in [None, '']):
        data += '<br>Altitude: ' + repr(article.altitude)
    if (data != ''):
        data += '</div>\n'
    return data

def itemToLinkHTML(article):
    data = ''
    if (article.sourceURL not in [None, '']):
        data += '<div class="linkDiv"><span class="itemTitle">'
        data += '<a href="' + article.sourceURL + \
            '" title="' + article.title + '" target="viewLink">' + article.title + '</a></span>'
        if (len(article.content) > 0):
            data += '<p>' + article.content
        data += '<div>'
    return data

def itemToListHTML(article, page, showDate = True):
    # TODO: Screen guestbook links and make sure to set rel="nofollow"
    # TODO-R: Refactor this method... it's pretty ugly and inflexible
    data = ''
    if (len(article.content) > 2):
        data += '<div class="innerBoxTitle">\n'
        data += createLink(str(article.id), '', '&nbsp;', inPage=True) + '\n'
        if ((article.sourceURL != '') and (article.hideAddress not in TRUE)):
            data += createLink(str(article.sourceURL), 'View link',
                '<span class="itemTitle">' + safeText(article.title) + '</span>',
                target='view_news', noFollow=(page.pageType == PAGE_GUESTBOOK))
        else:
            data += '<span class="itemTitle">' + safeText(article.title) + '</span>'
        if (showDate and APPLICATION.articleDate):
            data += '<span class="date">' + article.getSimpleDateString() + '</span>'
        data += '</div>\n'
        data += '<div class="innerBox">\n'
        if ((len(article.attachments) > 0) and (article.attachments[0].image in TRUE)):
            data += itemGetSmallImageHTML(article)
        data += '<span class="' + PAGE_TYPE_STYLES[page.pageType] + '">'
        data +='<p class="firstParagraph">\n'
        if (article.content[0] not in ['<', '&']):
            data +='<FONT CLASS="firstLetter">' + safeText(article.content[0]) + '</FONT>'
            data += safeText(article.content[1:]).replace('<p>', '\n<p>') + '\n'
        else:
            data += safeText(article.content[0:]).replace('<p>', '\n<p>') + '\n'
        data += '</span>\n'
        data += '<div class="articleFooter">\n'
        data += getAuthorHTML(article)
        if ((page.pageType != PAGE_GUESTBOOK) and
                (article.hideAddress not in TRUE) and
                (article.sourceName != '') and
                (article.sourceURL != '') and
                (article.sourceURL.find('http://') > -1)):
            data += '<br>source / reference link: ' + createLink(article.sourceURL,
                article.sourceName, article.sourceName, target='view_news') + '\n'
        data += getAddressHTML(article)
        data += getCoordinateHTML(article)
        if ((len(article.attachments) > 0) and (article.attachments[0].image not in TRUE)):
            data += '<br>' + createLink(APPLICATION.attachURL + article.attachments[0].filename, \
                article.attachments[0].notes, article.attachments[0].notes, target = 'attachment') + '<br>'
        if (page.allowComments or
                ((page.pageType == PAGE_BLOG) and (article.isOld(BLOG_COMMENTS_OLD) != True))):
            if (page.pageType == PAGE_GUESTBOOK):
                tprompt = 'Follow up on this article'
            else:
                tprompt = page.promptComments
            for item in article.comments:
                data += commentToHTML(item)
            data += '<br>' + createPopupLink(tprompt, tprompt,
                getCommentsForm(page.name, article.id), clazz='comment') + '\n'
        if (page.pageType == PAGE_GUESTBOOK):
            data += '<br>' + createPopupLink(page.promptComments, page.promptComments,
                getGuestbookForm(page.name, article.id), clazz='guestbook') + '\n'
        data += '</div>\n' #articleFooter

        if (APPLICATION.showAds):
            if (random.random() < AD_CHANCE):
                data += '<br/>&nbsp;<br/>\n'
                data += generateAdTermsHorizontal()
        data += '</div>\n' #innerBox
    return str(data)

def getCommentsForm(pageName, articleId):

    fbody = createHiddenInput('page', pageName) + '\n'
    fbody += createHiddenInput('itemId', articleId) + '\n'
    fbody += createHiddenInput('curlocation', '') + '\n'
    fbody += '<table border="0" cellspacing="0" cellpadding="3">\n'
    fbody += '<tr><td colspan="2"><h2>Submit a comment:</h2>\n'
    fbody += '<tr><th>Name:<td>' + createTextInput('tname', maxLength = 50) + '\n'
    fbody += '<tr><th>Email or web page:<td>' + createTextInput('email', maxLength = 100) + \
        ' &nbsp; ' + createCheckBox('hideAddress', 'True', True) + ' hide my address\n'
    fbody += '<tr><th>Comment:<td>' + createTextArea('comment', '', 10, 50, 400, 'commentForm' + str(articleId))
    fbody += '<tr><td colspan="2" align="right">' + \
        createLink('javascript:submitCommentForm(\'commentForm' + str(articleId) + '\');', 'Submit your comment', 'submit') + '\n'
    fbody += '</table>'

    data = createForm('commentForm' + str(articleId), '${adminURL}submit_comment.py',
        'POST', fbody)

    return data

def getGuestbookForm(pageName, articleId):

    fbody = createHiddenInput('page', pageName) + '\n'
    fbody += createHiddenInput('curlocation', '') + '\n'
    fbody += '<table border="0" cellspacing="0" cellpadding="3">\n'
    fbody += '<tr><td colspan="2"><h2>Submit a comment:</h2>\n'
    fbody += '<tr><th>Name:<td>' + createTextInput('tname', maxLength = 50) + '\n'
    fbody += '<tr><th>Email or web page:<td>' + createTextInput('email', maxLength = 100) + \
        ' &nbsp; ' + createCheckBox('hideAddress', 'True', True) + ' hide my address\n'
    fbody += '<tr><th>Subject:<td>' + createTextInput('title', maxLength = 50) + '\n'
    fbody += '<tr><th>Comment:<td>' + createTextArea('comment', '', 10, 50, 400, 'guestbookForm' + str(articleId))
    fbody += '<tr><td colspan="2" align="right">' + \
        createLink('javascript:submitGuestbookForm(\'guestbookForm' + str(articleId) + '\');', 'Submit your comment', 'submit') + '\n'
    fbody += '</table>'

    data = createForm('guestbookForm' + str(articleId), '${adminURL}submit_guestbook.py',
        'POST', fbody)

    return data

def commentToHTML(comment):
    data = '<div class="comment">\n'
    data += '<span class="date">' + comment.createdDate.strftime('%B %d, %Y %H:%M') + '</span>\n'
    data += '<p>' + comment.content + '\n'
    data += '<br> -- '
    if (comment.hideAddress not in TRUE):
        if (comment.email.lower().find('@') > 0):
            data += createLink("mailto:" + comment.email, comment.email, comment.name)
        else:
            data += createLink(comment.email, comment.email, comment.name)
    else:
        data += comment.name
    data += '\n</div>\n'
    return data

def itemGetSmallImageHTML(article, attachment = 0):
    #<img src="http://localhost/cgi-bin/yj/somesite/load_image.py?id=somejpg.jpg&type=JPG">

    imgSrc = APPLICATION.adminURL + 'load_image.py?id=' + article.attachments[attachment].filename + \
        '&type=' + str(article.attachments[attachment].filename[len(article.attachments[attachment].filename)-3:]).upper()
    thumbnailImgSrc = APPLICATION.adminURL + 'load_image.py?id=' + article.attachments[attachment].thumbnailName + \
        '&type=' + str(article.attachments[attachment].filename[len(article.attachments[attachment].filename)-3:]).upper()

    data = '<DIV CLASS="' + str(article.attachments[attachment].align) + \
        '"><A HREF="' + imgSrc + \
        '" TARGET="imageWin" TITLE="' + article.attachments[attachment].notes + \
        '"><IMG SRC="' + thumbnailImgSrc + \
        '" HEIGHT="' + str(article.attachments[attachment].thumbnailHeight) + '" WIDTH="' + \
        str(article.attachments[attachment].thumbnailWidth) + \
        '" ></A><BR>' + article.attachments[attachment].notes + '</DIV>'
    return data

def itemToHeadlineVerboseHTML(article, headlineType, articleURL):
    data = ''
    if (len(article.content) > 2):
        data = '<p>' + '<a href="' + articleURL + '#' + str(article.id) + \
            '" title="more" class="more"><span class="articleTitle">' + article.title + '</span></a>\n'
        if (APPLICATION.articleDate):
            data += '<span class="date">' + article.getSimpleDateString() + '</span>\n'
        tcontent = article.content
        if ((tcontent is not None) and (tcontent != '') and (tcontent != 'None')):
            if (headlineType == HEADLINE_VERBOSE):
                stripper = Stripper()
                tcontent = tcontent[0:350] + stripper.strip(tcontent[350:])
                data += '<p>' + safeText(tcontent[0:500]) + \
                    '... <a href="' + articleURL + '#' + str(article.id) + \
                    '" title="more" class="more">' + APPLICATION.moreText + '</a>\n'
            else:
                data += '<p>' + safeText(article.content[0:]) + \
                    '... <a href="' + articleURL + '#' + str(article.id) + \
                    '" title="more" class="more">' + APPLICATION.moreText + '</a>\n'
    return str(data)

def itemToHeadlineListHTML(article, articleURL, imageUrl = None):
    data = '<p><a href="' + articleURL + '#' + str(article.id) + \
            '" title="' + safeText(article.title) + '"><span class="articleTitle">' + \
            safeText(article.title) + '</span></a>\n'
    if (APPLICATION.articleDate):
        data += '<span class="date">' + article.getSimpleDateString() + '</span>\n'
    tcontent = safeText(unicode(article.content))
    if ((tcontent is not None) and (tcontent != '') and (tcontent != 'None')):
        stripper = Stripper()
        tcontent = stripper.strip(tcontent)
        data += '<p>' + safeText(tcontent[0:90]) + '...\n'
    data += ' <a href="' + articleURL + '#' + str(article.id) + \
        '" title="more" class="more">' + APPLICATION.moreText + '</a>\n'
    return str(data)

def itemToHeadlineOnlyHTML(article, pageURL):
    data = ''
    if (len(article.content) > 2):
        data = '<p>' + \
            ' <a href="' + pageURL + '#' + str(article.id) + \
            '" title="' + safeText(article.title) + '"><span class="articleTitle">' +\
            safeText(article.title) + '</span></a>\n'
    return str(data)

def itemToBriefSearchHTML(article, pageURL, searchTerms = None, treatAsPhrase = False):
    data = ''
    searchData = ''
    if (searchTerms is not None):
        searchData = '?searchTerms=' + searchTerms
        if (treatAsPhrase):
            searchData += '&treatAsPhrase=true'
    if (len(article.content) > 2):
        data = '<p>' + \
            ' <a href="' + pageURL + searchData + '&id=#' + str(article.id) + \
            '" title="' + safeText(article.title) + '"><span class="searchTitle">' +\
            safeText(article.title) + '</span></a>\n'
    return str(data)

def itemToVerboseSearchHTML(article, pageURL, imageUrl = None, searchTerms = None, treatAsPhrase = False):
    searchData = ''
    if (searchTerms is not None):
        searchData = '?searchTerms=' + searchTerms
        if (treatAsPhrase):
            searchData += '&treatAsPhrase=true'
    data = '<p><a href="' + pageURL + searchData + '&id=#' + str(article.id) + \
            '" title="' + safeText(article.title) + '"><span class="searchTitle">' + \
            safeText(article.title) + '</span></a>\n'
    if (APPLICATION.articleDate):
        data += ' - <span class="searchDate">' + article.getSimpleDateString() + '</span>\n'
    tcontent = safeText(unicode(article.content))
    if ((tcontent is not None) and (tcontent != '') and (tcontent != 'None')):
        stripper = Stripper()
        tcontent = stripper.strip(tcontent)
        data += '<br><span class="searchText">' + safeText(tcontent[0:90]) + '...</span>\n'
    return str(data)

# Classes
