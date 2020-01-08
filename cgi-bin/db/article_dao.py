
# imports
from newscommunity.application import APPLICATION
from newscommunity.ncvars import *
from newspage_dao import *
from comment_dao import *
from attachment_dao import *
from utils import *
import re

# declarations

# definitions

# classes

class Article:
    ''' Basic article DTO.  Contains some functionality methods. '''

    def __init__(self, id=None):
        self.id = id
        self.title = ''
        self.content = ''
        self.hideAddress = False
        self.published = True
        self.expired = False
        self.latitude = None
        self.longitude = None
        self.altitude = None
        self.street = ''
        self.street2 = ''
        self.city = ''
        self.state = ''
        self.zip = ''
        self.country = ''
        self.phone = ''
        self.keywords = ''
        self.category = ''
        self.sourceName = ''
        self.sourceURL = ''
        self.language = ''
        self.publishedDate = None
        self.createdBy = ''
        self.createdDate = None
        self.modifiedBy = ''
        self.modifiedDate = None

        self.newspageArticleId = None
        self.newspageName = None

        self.attachments = list()

        self.comments = list()

    def search(self, searchTerms, findAllTerms = False, caseSensitive = False):
        '''Search the article for a given search term or terms.

            searchTerms - a list of search terms
            findAllTerms - 'and' the search terms
            caseSensitive - case sensitive search

            returns True if the article contains the terms
        '''

        check = self.published

        if (not isinstance(searchTerms, list)):
            searchTerms = [searchTerms]

        if (check):
            terms = list()

            if (findAllTerms):
                terms = searchTerms
            else:
                tmp = ''
                for item in searchTerms:
                    if (tmp != ''):
                        tmp += '|'
                    tmp += item
                terms = [tmp]

            for term in terms:
                if (caseSensitive):
                    check2 = ((re.search(term, self.title) is not None) or \
                        (re.search(term, self.content) is not None) or \
                        (re.search(term, self.category) is not None) or \
                        (re.search(term, self.sourceName) is not None) or \
                        (re.search(term, self.sourceURL) is not None) or \
                        (re.search(term, self.createdBy) is not None))
                else:
                    term = term.lower()
                    check2 = ((re.search(term, self.title.lower()) is not None) or \
                        (re.search(term, self.content.lower()) is not None) or \
                        (re.search(term, self.category.lower()) is not None) or \
                        (re.search(term, self.sourceName.lower()) is not None) or \
                        (re.search(term, self.sourceURL.lower()) is not None) or \
                        (re.search(term, self.createdBy.lower()) is not None))
                check = check and check2

        return check

    def setPublishedDate(self, year, month, day, hour, minute):
        self.publishedDate = datetime.datetime(year, month, day, hour, minute)

    def setCreatedDate(self, year, month, day, hour, minute):
        self.createdDate = datetime.datetime(year, month, day, hour, minute)

    def setModifiedDate(self, year, month, day, hour, minute):
        self.modifiedDate = datetime.datetime(year, month, day, hour, minute)

    def getSimpleDateString(self, pubDate = True):
        ''' Get the display date as a simple date string
            "June 14, 2005 13:03"
            If pubDate == False, then this will return the date
            for the last-modified date.
        '''
        data = ''
        if (pubDate):
            data = self.publishedDate.strftime('%B %d, %Y %H:%M')
        else:
            if (self.modifiedDate is None):
                if (self.createdDate is not None):
                    data = self.createdDate.strftime('%B %d, %Y %H:%M')
            else:
                data = self.modifiedDate.strftime('%B %d, %Y %H:%M')
        return str(data)

    def getXMLDateString(self, pubDate = True):
        ''' Get an XML Date string to be used in the written out files.
            If displayDate == False, then this will return the XML date
            for the last-modified date.
        '''
        data = ''
        if (pubDate):
            data = self.publishedDate.strftime('%m %d %Y %H:%M')
        else:
            if (self.modifiedDate is None):
                if (self.createdDate is not None):
                    data = self.createdDate.strftime('%m %d %Y %H:%M')
            else:
                data = self.modifiedDate.strftime('%m %d %Y %H:%M')
        return str(data)

    def getDateAsInt(self, pubDate = True):
        '''Get the display date as an int of seconds (ordinal date).
            If publishedDate == False, then this will return the ordinal date
            for the last-modified date.

            This stuff is contorted because I added in the LastModified date late.
        '''

        data = 0
        if (pubDate):
            data = self.publishedDate.toordinal()
        else:
            if (self.modifiedDate is None):
                data = self.createdDate.toordinal()
            else:
                data = self.modifiedDate.toordinal()
        return data

    def isOld(self, days, pubDate = True):
        ''' Check to see if the item's published date (or last-modified
            date if publishedDate == False) is older than 'days' old.
        '''
        curtime = datetime.datetime.today().toordinal()
        checktime = 0
        if (pubDate):
            checktime = self.publishedDate.toordinal()
        else:
            if (self.modifiedDate is None):
                checktime = self.createdDate.toordinal()
            else:
                checktime = self.modifiedDate.toordinal()
        return ((curtime - checktime) > days)

    def __str__(self):
        data = 'Article instance:\r\n'
        for item in self.__dict__:
            data += '\t' + item + ':' + str(self.__dict__[item]) + '\r\n'
        return data


class ArticleDaoFactory:
    ''' Factory class for creating DAO objects to load articles. '''

    def create(cls, apID = None):
        ''' Create the DAO. '''
        return ArticleDaoImpl(apID)

    # TODO-L: If server converts to Python 2.4, change to function decorator
    create = classmethod(create)

class ArticleDao(ConnectionAwareObject):
    ''' Base class for objects that will be used to query the DB to retrieve
        Article information. Use this class as the ancestor for impl or mock
        test classes. '''

    def __init__(self, apID = None):
        ConnectionAwareObject.__init__(self)

    def fetchByID(self, id):
        ''' Get an article using it's id. '''
        raise Exception('Not implemented')

    def fetchAll(self, newspageName = None, notExpired = True):
        ''' Get all the articles for the given Newspage registered with the DAO. '''
        raise Exception('Not implemented')

    def fetchSorted(self, newspageName = None, sortType = SORT_DATE, limit=0, publishedOnly=False, notExpired=True):
        ''' Get a sorted list of articles.
            Setting a value > 0 for limit will limit the total number of
            results that comes back to that number (or less).
            Returns a list of Article instances.
        '''
        raise Exception('Not implemented')

    def fetchByNewestPublished(self, newspageName = None, limit = 0, publishedOnly = False, notExpired = True):
        ''' Get a list of articles with the newest first.
            Setting a value > 0 for limit will limit the total number of
            results that comes back to that number (or less).
            Returns a list of Article instances.
        '''
        raise Exception('Not implemented')

    def fetchByOldestPublished(self, newspageName = None, limit = 0, publishedOnly = False, notExpired = True):
        ''' Get a list of articles with the oldest first.
            Setting a value > 0 for limit will limit the total number of
            results that comes back to that number (or less).
            Returns a list of Article instances.
        '''
        raise Exception('Not implemented')

    def fetchByNewestModified(self, newspageName = None, limit = 0, publishedOnly = False, notExpired = True):
        ''' Get a list of articles with the newest first.
            Setting a value > 0 for limit will limit the total number of
            results that comes back to that number (or less).
            Returns a list of Article instances.
        '''
        raise Exception('Not implemented')

    def fetchByOldestModified(self, newspageName = None, limit = 0, publishedOnly = False, notExpired = True):
        ''' Get a list of articles with the oldest first.
            Setting a value > 0 for limit will limit the total number of
            results that comes back to that number (or less).
            Returns a list of Article instances.
        '''
        raise Exception('Not implemented')

    def fetchByAlpha(self, newspageName = None, limit = 0, publishedOnly = False, notExpired = True):
        ''' Get a list of articles sorted alphabetically by title.
            Setting a value > 0 for limit will limit the total number of
            results that comes back to that number (or less).
            Returns a list of Article instances.
        '''
        raise Exception('Not implemented')

    def fetchByReverseAlpha(self, newspageName = None, limit = 0, publishedOnly = False, notExpired = True):
        ''' Get a list of articles sorted alphabetically by title.
            Setting a value > 0 for limit will limit the total number of
            results that comes back to that number (or less).
            Returns a list of Article instances.
        '''
        raise Exception('Not implemented')

    def write(self, article):
        ''' Write an article to the db.  The article should be inserted
            if it's new or updated, if it already exists.
        '''
        raise Exception('Not implemented')

    def countByNewspage(self, newspageName, countNotPublished = False):
        ''' Count the number of articles in the newspage.

            return the number counted
        '''
        raise Exception('Not implemented')

    def delete(self, article):
        ''' Delete a particular article. '''
        raise Exception('Not implemented')

    def deleteByNewspage(self, newspageName):
        ''' Delete all the articles in a Newspage. '''
        raise DaoException('Not implemented')

    def expire(self, days):
        ''' Expire all articles that are older than 'days' old. '''
        raise Exception('Not implemented')

    def search(self, newspageName, sortType, searchTerms, findAllTerms = False, caseSensitive = False, limit = 50):
        ''' Delete all articles that are older than 'days' old. '''
        raise Exception('Not implemented')

    def buildCountReport(self):
        ''' Build a report showing:

                newspageName, total articles, articles pending

            sorted by newapage name.

            returns a list of tuples (string, int, int)
        '''
        raise Exception('Not implemented')

class ArticleDaoImpl(ArticleDao):
    ''' MySQL impl class for objects that will be used to query the DB to retrieve
        Article information. Use this class as the ancestor for impl or mock
        test classes. '''

    TABLE_ARTICLE = 'article' + '_${ID}'
    TABLE_NEWSPAGE_ARTICLE = 'newspage_article' + '_${ID}'

    # ARTICLE columns
    A_ID = 'id'
    A_TITLE = 'title'
    A_CONTENT = 'content'
    A_HIDE_ADDRESS = 'hide_address'
    A_PUBLISHED = 'published'
    A_EXPIRED = 'expired'
    A_LATITUDE = 'latitude'
    A_LONGITUDE = 'longitude'
    A_ALTITUDE = 'altitude'
    A_STREET = 'street'
    A_STREET2 = 'street2'
    A_CITY = 'city'
    A_STATE = 'state'
    A_ZIP = 'zip'
    A_COUNTRY = 'country'
    A_PHONE = 'phone'
    A_KEYWORDS = 'keywords'
    A_CATEGORY = 'category'
    A_SOURCE_NAME = 'source_name'
    A_SOURCE_URL = 'source_url'
    A_LANGUAGE_ID = 'language_id'
    A_PUBLISHED_DATE = 'published_date'
    A_CREATED_BY = 'created_by'
    A_CREATED_DATE = 'created_date'
    A_MODIFIED_BY = 'modified_by'
    A_MODIFIED_DATE = 'modified_date'

    # NEWSPAGE_ARTICLE columns
    NA_ID = 'id'
    NA_ARTICLE_ID = 'article_id'
    NA_NEWSPAGE_NAME = 'newspage_name'

    SELECT = 'SELECT '
    DISTINCT = 'DISTINCT '
    FROM = 'FROM '
    WHERE = 'WHERE '
    AND = 'AND '
    COUNT = 'COUNT(*) '

    ORDER_BY_PUBLSHED_DATE_ASC = 'ORDER BY a.' + A_PUBLISHED_DATE + ' ASC '
    ORDER_BY_PUBLSHED_DATE_DESC = 'ORDER BY a.' + A_PUBLISHED_DATE + ' DESC '
    ORDER_BY_MODIFIED_DATE_ASC = 'ORDER BY a.' + A_MODIFIED_DATE + ' ASC '
    ORDER_BY_MODIFIED_DATE_DESC = 'ORDER BY a.' + A_MODIFIED_DATE + ' DESC '
    ORDER_BY_TITLE_ASC = 'ORDER BY a.' + A_TITLE + ' ASC '
    ORDER_BY_TITLE_DESC = 'ORDER BY a.' + A_TITLE + ' DESC '
    ORDER_BY_NEWSPAGE_NAME = 'ORDER BY b.' + NA_NEWSPAGE_NAME + ' '
    LIMIT = 'LIMIT %s '

    SELECT_COLUMNS = 'a.' + A_ID + ', ' + A_TITLE + ', ' + A_CONTENT + ', ' + \
        A_HIDE_ADDRESS + ', ' + A_PUBLISHED + ', ' + A_EXPIRED + ', ' + A_LATITUDE + ', ' + \
        A_LONGITUDE + ', ' + A_ALTITUDE + ', ' + A_STREET + ', ' + A_STREET2 + ', ' + \
        A_CITY + ', ' + A_STATE + ', ' + A_ZIP + ', ' + A_COUNTRY + ', ' + A_PHONE + ', ' + \
        A_KEYWORDS + ', ' + A_CATEGORY + ', ' + A_SOURCE_NAME + ', ' + A_SOURCE_URL + ', ' + \
        A_LANGUAGE_ID + ', ' + A_PUBLISHED_DATE + ', ' + A_CREATED_BY + ', ' + \
        A_CREATED_DATE + ', ' + A_MODIFIED_BY + ', ' + A_MODIFIED_DATE + ', ' + \
        'b.' + NA_NEWSPAGE_NAME + ', ' + 'b.' + NA_ID + ' newspage_article_id '

    SELECT_TABLES = TABLE_ARTICLE + ' a, ' + TABLE_NEWSPAGE_ARTICLE + ' b '
    WHERE_JOIN = 'a.' + A_ID + ' = ' + 'b.' + NA_ARTICLE_ID + ' '
    WHERE_NEWSPAGE = 'b.' + NA_NEWSPAGE_NAME + ' = %s '
    WHERE_ID = 'a.' + A_ID + ' = %s '
    WHERE_PUBLISHED = 'a.' + A_PUBLISHED + ' = 1 '
    WHERE_NOT_PUBLISHED = 'a.' + A_PUBLISHED + ' = 0 '
    WHERE_EXPIRED = 'a.' + A_EXPIRED + ' = 1 '
    WHERE_NOT_EXPIRED = 'a.' + A_EXPIRED + ' = 0 '

    SELECT_ALL = SELECT + SELECT_COLUMNS + FROM + \
        SELECT_TABLES + WHERE + WHERE_JOIN

    SELECT_BY_ID = SELECT + SELECT_COLUMNS + FROM + \
        SELECT_TABLES + WHERE + WHERE_JOIN + AND + WHERE_ID

    SELECT_COUNT_ALL = SELECT + COUNT + FROM + SELECT_TABLES + WHERE + \
        WHERE_JOIN + AND + WHERE_NEWSPAGE

    SELECT_COUNT_NOT_PUBLISHED = SELECT + COUNT + FROM + SELECT_TABLES + WHERE + \
        WHERE_JOIN + AND + WHERE_NEWSPAGE + AND + WHERE_NOT_PUBLISHED

    SELECT_COUNT_EXPIRED = SELECT + COUNT + FROM + SELECT_TABLES + WHERE + \
        WHERE_JOIN + AND + WHERE_NEWSPAGE + AND + WHERE_EXPIRED

    SELECT_NEWSPAGE_NAMES = SELECT + DISTINCT + NA_NEWSPAGE_NAME + ' ' + FROM + SELECT_TABLES + WHERE + WHERE_JOIN + ORDER_BY_NEWSPAGE_NAME

    # INSERT variables

    INSERT = 'INSERT '
    INTO = 'INTO '
    VALUES = 'VALUES'
    ON_DUPLICATE_KEY_UPDATE = 'ON DUPLICATE KEY UPDATE '

    ARTICLE_INSERT_COLUMNS = A_ID + ', ' + A_TITLE + ', ' + A_CONTENT + ', ' + \
        A_HIDE_ADDRESS + ', ' + A_PUBLISHED + ', ' + A_EXPIRED + ', ' + A_LATITUDE + ', ' + \
        A_LONGITUDE + ', ' + A_ALTITUDE + ', ' + A_STREET + ', ' + A_STREET2 + ', ' + \
        A_CITY + ', ' + A_STATE + ', ' + A_ZIP + ', ' + A_COUNTRY + ', ' + A_PHONE + ', ' + \
        A_KEYWORDS + ', ' + A_CATEGORY + ', ' + A_SOURCE_NAME + ', ' + A_SOURCE_URL + ', ' + \
        A_LANGUAGE_ID + ', ' + A_PUBLISHED_DATE + ', ' + A_CREATED_BY + ', ' + \
        A_CREATED_DATE + ', ' + A_MODIFIED_BY + ', ' + A_MODIFIED_DATE

    INSERT_ARTICLE = INSERT + INTO + TABLE_ARTICLE + '(' + \
        ARTICLE_INSERT_COLUMNS + ') ' + VALUES + \
        '(%s, %s, %s, %s, %s, %s, ' + \
        '%s, %s, %s, %s, %s, ' + \
        '%s, %s, %s, %s, %s, ' + \
        '%s, %s, %s, %s, %s, ' + \
        '%s, %s, %s, %s, %s) ' + \
        ON_DUPLICATE_KEY_UPDATE + \
        A_TITLE + '=' + VALUES + '(' + A_TITLE + '), ' + \
        A_CONTENT + '=' + VALUES + '(' + A_CONTENT + '), ' + \
        A_HIDE_ADDRESS + '=' + VALUES + '(' + A_HIDE_ADDRESS + '), ' + \
        A_PUBLISHED + '=' + VALUES + '(' + A_PUBLISHED + '), ' + \
        A_EXPIRED + '=' + VALUES + '(' + A_EXPIRED + '), ' + \
        A_LATITUDE + '=' + VALUES + '(' + A_LATITUDE + '), ' + \
        A_LONGITUDE + '=' + VALUES + '(' + A_LONGITUDE + '), ' + \
        A_ALTITUDE + '=' + VALUES + '(' + A_ALTITUDE + '), ' + \
        A_STREET + '=' + VALUES + '(' + A_STREET + '), ' + \
        A_STREET2 + '=' + VALUES + '(' + A_STREET2 + '), ' + \
        A_CITY + '=' + VALUES + '(' + A_CITY + '), ' + \
        A_STATE + '=' + VALUES + '(' + A_STATE + '), ' + \
        A_ZIP + '=' + VALUES + '(' + A_ZIP + '), ' + \
        A_COUNTRY + '=' + VALUES + '(' + A_COUNTRY + '), ' + \
        A_PHONE + '=' + VALUES + '(' + A_PHONE + '), ' + \
        A_KEYWORDS + '=' + VALUES + '(' + A_KEYWORDS + '), ' + \
        A_CATEGORY + '=' + VALUES + '(' + A_CATEGORY + '), ' + \
        A_SOURCE_NAME + '=' + VALUES + '(' + A_SOURCE_NAME + '), ' + \
        A_SOURCE_URL + '=' + VALUES + '(' + A_SOURCE_URL + '), ' + \
        A_LANGUAGE_ID + '=' + VALUES + '(' + A_LANGUAGE_ID + '), ' + \
        A_PUBLISHED_DATE + '=' + VALUES + '(' + A_PUBLISHED_DATE + '), ' + \
        A_CREATED_BY + '=' + VALUES + '(' + A_CREATED_BY + '), ' + \
        A_CREATED_DATE + '=' + VALUES + '(' + A_CREATED_DATE + '), ' + \
        A_MODIFIED_BY + '=' + VALUES + '(' + A_MODIFIED_BY + '), ' + \
        A_MODIFIED_DATE + '=' + VALUES + '(' + A_MODIFIED_DATE + ')'

    NEWSPAGE_ARTICLE_INSERT_COLUMNS = NA_ID + ', ' + NA_ARTICLE_ID + ', ' + NA_NEWSPAGE_NAME + ' '

    INSERT_NEWSPAGE_ARTICLE = INSERT + INTO + TABLE_NEWSPAGE_ARTICLE + '(' + \
        NEWSPAGE_ARTICLE_INSERT_COLUMNS + ') ' + VALUES + \
        '(%s, %s, %s) ' + \
        ON_DUPLICATE_KEY_UPDATE + \
        NA_NEWSPAGE_NAME + '=' + VALUES + '(' + NA_NEWSPAGE_NAME + ')'

    # DELETE variables

    DELETE = 'DELETE '

    WHERE_DELETE_ARTICLE = A_ID + ' = %s '

    DELETE_ARTICLE = DELETE + FROM + TABLE_ARTICLE + ' ' + WHERE + WHERE_DELETE_ARTICLE

    DELETE_ARTICLE_BY_NEWSPAGE = DELETE + FROM + TABLE_ARTICLE + ' ' + WHERE + A_ID + ' in (' + \
        SELECT + NA_ARTICLE_ID + ' ' + FROM + TABLE_NEWSPAGE_ARTICLE + ' b ' + WHERE + WHERE_NEWSPAGE + ')'

    # utility vars
    applicationID = None

    def __init__(self, apID = None):
        ArticleDao.__init__(self)
        if (apID is None):
            self.applicationID = APPLICATION.ID
        else:
            self.applicationID = apID
        self.__setUpQueries()

    def __setUpQueries(self):
        # Replace the table names with table_name_[site id number]
        self.SELECT_ALL = self.SELECT_ALL.replace('${ID}', str(self.applicationID))
        self.SELECT_BY_ID = self.SELECT_BY_ID.replace('${ID}', str(self.applicationID))
        self.SELECT_COUNT_ALL = self.SELECT_COUNT_ALL.replace('${ID}', str(self.applicationID))
        self.SELECT_COUNT_NOT_PUBLISHED = self.SELECT_COUNT_NOT_PUBLISHED.replace('${ID}', str(self.applicationID))
        self.SELECT_COUNT_EXPIRED = self.SELECT_COUNT_EXPIRED.replace('${ID}', str(self.applicationID))
        self.SELECT_NEWSPAGE_NAMES = self.SELECT_NEWSPAGE_NAMES.replace('${ID}', str(self.applicationID))
        self.INSERT_ARTICLE = self.INSERT_ARTICLE.replace('${ID}', str(self.applicationID))
        self.INSERT_NEWSPAGE_ARTICLE = self.INSERT_NEWSPAGE_ARTICLE.replace('${ID}', str(self.applicationID))
        self.DELETE_ARTICLE = self.DELETE_ARTICLE.replace('${ID}', str(self.applicationID))
        self.DELETE_ARTICLE_BY_NEWSPAGE = self.DELETE_ARTICLE_BY_NEWSPAGE.replace('${ID}', str(self.applicationID))

    def __populateDto(self, article, data):
        ''' Populate a DTO given a return result. '''

        if ((data is None) or (len(data) == 0)):
            raise DaoException("Unexpectedly got None or zero for data")

        i = 0
        article.id = data[i]; i += 1
        article.title = data[i]; i += 1
        article.content = data[i]; i += 1
        article.hideAddress = (data[i] in TRUE); i += 1
        article.published = (data[i] in TRUE); i += 1
        article.expired = (data[i] in TRUE); i += 1
        article.latitude = data[i]; i += 1
        article.longitude = data[i]; i += 1
        article.altitude = data[i]; i += 1
        article.street = data[i]; i += 1
        article.street2 = data[i]; i += 1
        article.city = data[i]; i += 1
        article.state = data[i]; i += 1
        article.zip = data[i]; i += 1
        article.country = data[i]; i += 1
        article.phone = data[i]; i += 1
        article.keywords = data[i]; i += 1
        article.category = data[i]; i += 1
        article.sourceName = data[i]; i += 1
        article.sourceURL = data[i]; i += 1
        article.language = data[i]; i += 1
        article.publishedDate = data[i]; i += 1
        article.createdBy = data[i]; i += 1
        article.createdDate = data[i]; i += 1
        article.modifiedBy = data[i]; i += 1
        article.modifiedDate = data[i]; i += 1

        article.newspageName = data[i]; i += 1
        article.newspageArticleId = data[i]

    def __populateAttachmentsAndComments(self, article):
            commentDao = CommentDaoFactory.create(self.applicationID)
            attachmentDao = AttachmentDaoFactory.create(self.applicationID)
            try:
                article.comments = commentDao.fetchByArticleID(article.id)
                article.attachments = attachmentDao.fetchByArticleID(article.id)
            finally:
                commentDao.cleanUp()
                attachmentDao.cleanUp()

    def fetchByID(self, id):
        ''' Get an article using it's id.

            returns an article or None if no article was found
        '''
        article = None

        try:
            cursor = self.getCursor()
            self.lastSelect = self.SELECT_BY_ID
            retval = cursor.execute(self.SELECT_BY_ID, (id,))
            self.getConnection().commit()

            if (retval == 1):
                article = Article()
                self.__populateDto(article, cursor.fetchone())
                self.__populateAttachmentsAndComments(article)
            elif (retval > 1):
                raise DaoException('Unexpectedly returned ' + str(retval) + ' results on select')
        finally:
            self.releaseCursor()

        return article

    def fetchAll(self, newspageName = None, notExpired = True):
        ''' Get all the articles for the given Newspage registered with the DAO.
            By default, this will not return Expired articles.

            returns a list of articles or an empty list if no article was found
        '''
        articles = list()

        try:
            cursor = self.getCursor()
            self.lastSelect = self.SELECT_ALL
            if (newspageName is not None):
                self.lastSelect +=  self.AND + self.WHERE_NEWSPAGE
            if (notExpired):
                self.lastSelect += self.AND + self.WHERE_NOT_EXPIRED
            retval = cursor.execute(self.lastSelect, (newspageName,))
            self.getConnection().commit()

            if (retval > 0):
                for item in cursor.fetchall():
                    article = Article()
                    self.__populateDto(article, item)
                    self.__populateAttachmentsAndComments(article)
                    articles += [article]

        finally:
            self.releaseCursor()

        return articles

    def __fetchByOrder(self, orderClause, newspageName = None, limit = 0, publishedOnly = False, notExpired = True):
        ''' Utility method to simplify fetching in order.

            returns a list of articles or an empty list if no article was found
        '''
        articles = list()

        try:
            cursor = self.getCursor()
            self.lastSelect = self.SELECT_ALL
            if (newspageName is not None):
                self.lastSelect +=  self.AND + self.WHERE_NEWSPAGE
            if (publishedOnly):
                self.lastSelect += self.AND + self.WHERE_PUBLISHED
            if (notExpired):
                self.lastSelect += self.AND + self.WHERE_NOT_EXPIRED
            self.lastSelect += orderClause
            values = (newspageName,)
            if (limit > 0):
                self.lastSelect += self.LIMIT
                values += (limit,)

            retval = cursor.execute(self.lastSelect, values)
            self.getConnection().commit()

            if (retval > 0):
                for item in cursor.fetchall():
                    article = Article()
                    self.__populateDto(article, item)
                    self.__populateAttachmentsAndComments(article)
                    articles += [article]
        finally:
            self.releaseCursor()

        # DEBUG CODE ONLY
        #for item in articles:
        #    print 'Article id: ' + str(item.id) + ' ' + toMySqlDateString(item.publishedDate) + ' ' + \
        #        toMySqlDateString(item.createdDate) + ' ' + toMySqlDateString(item.modifiedDate)
        return articles

    def fetchSorted(self, newspageName = None, sortType = SORT_DATE, limit=0, publishedOnly=False, notExpired=True):
        ''' Get a sorted list of articles.
            Setting a value > 0 for limit will limit the total number of
            results that comes back to that number (or less).
            Returns a list of Article instances.
        '''
        articles = list()
        if(sortType == SORT_DATE):
            articles = self.fetchByNewestPublished(newspageName, limit, publishedOnly, notExpired)
        elif(sortType == SORT_DATE_REVERSE):
            articles = self.fetchByOldestPublished(newspageName, limit, publishedOnly, notExpired)
        elif(sortType == SORT_DATE_LM):
            articles = self.fetchByNewestModified(newspageName, limit, publishedOnly, notExpired)
        elif(sortType == SORT_DATE_REVERSE_LM):
            articles = self.fetchByOldestModified(newspageName, limit, publishedOnly, notExpired)
        elif(sortType == SORT_ALPHABETIC):
            articles = self.fetchByAlpha(newspageName, limit, publishedOnly, notExpired)
        elif(sortType == SORT_ALPHABETIC_REVERSE):
            articles = self.fetchByReverseAlpha(newspageName, limit, publishedOnly, notExpired)
        else:
            raise DaoException('Unexpected sort type: ' + sortType)
        return articles

    def fetchByNewestPublished(self, newspageName = None, limit = 0, publishedOnly = False, notExpired = True):
        ''' Get a list of articles with the newest first.
            Setting a value > 0 for limit will limit the total number of
            results that comes back to that number (or less).
            Returns a list of Article instances.

            returns a list of articles or an empty list if no article was found
        '''
        return self.__fetchByOrder(self.ORDER_BY_PUBLSHED_DATE_DESC, newspageName, limit, publishedOnly, notExpired)

    def fetchByOldestPublished(self, newspageName = None, limit = 0, publishedOnly = False, notExpired = True):
        ''' Get a list of articles with the oldest first.
            Setting a value > 0 for limit will limit the total number of
            results that comes back to that number (or less).
            Returns a list of Article instances.

            returns a list of articles or an empty list if no article was found
        '''
        return self.__fetchByOrder(self.ORDER_BY_PUBLSHED_DATE_ASC, newspageName, limit, publishedOnly, notExpired)

    def fetchByNewestModified(self, newspageName = None, limit = 0, publishedOnly = False, notExpired = True):
        ''' Get a list of articles with the newest first.
            Setting a value > 0 for limit will limit the total number of
            results that comes back to that number (or less).
            Returns a list of Article instances.

            returns a list of articles or an empty list if no article was found
        '''
        return self.__fetchByOrder(self.ORDER_BY_MODIFIED_DATE_DESC, newspageName, limit, publishedOnly, notExpired)

    def fetchByOldestModified(self, newspageName = None, limit = 0, publishedOnly = False, notExpired = True):
        ''' Get a list of articles with the oldest first.
            Setting a value > 0 for limit will limit the total number of
            results that comes back to that number (or less).
            Returns a list of Article instances.

            returns a list of articles or an empty list if no article was found
        '''
        return self.__fetchByOrder(self.ORDER_BY_MODIFIED_DATE_ASC, newspageName, limit, publishedOnly, notExpired)

    def fetchByAlpha(self, newspageName = None, limit = 0, publishedOnly = False, notExpired = True):
        ''' Get a list of articles sorted alphabetically by title.
            Setting a value > 0 for limit will limit the total number of
            results that comes back to that number (or less).
            Returns a list of Article instances.

            returns a list of articles or an empty list if no article was found
        '''
        return self.__fetchByOrder(self.ORDER_BY_TITLE_ASC, newspageName, limit, publishedOnly, notExpired)

    def fetchByReverseAlpha(self, newspageName = None, limit = 0, publishedOnly = False, notExpired = True):
        ''' Get a list of articles sorted alphabetically by title.
            Setting a value > 0 for limit will limit the total number of
            results that comes back to that number (or less).
            Returns a list of Article instances.

            returns a list of articles or an empty list if no article was found
        '''
        return self.__fetchByOrder(self.ORDER_BY_TITLE_DESC, newspageName, limit, publishedOnly, notExpired)

    def write(self, article):
        ''' Write an article to the db.  The article should be inserted
            if it's new or updated, if it already exists.

            returns the lastrowid from the insert or update
        '''

        if (article.id <= 0):
            article.id = None

        if (article.newspageName is None):
            raise DaoException('Article newspage name cannot be None')

        try:
            cursor = self.getCursor()

            modDate = None
            if (article.modifiedDate is not None):
                modDate = toMySqlDateString(article.modifiedDate)

            # Note: I took out calls to safeMySqlEscapeString because the slashes were being generated redundantly
            self.lastSelect = self.INSERT_ARTICLE
            valuesTuple = (article.id,
                article.title,
                article.content,
                toMySqlBoolean(article.hideAddress),
                toMySqlBoolean(article.published),
                toMySqlBoolean(article.expired),
                article.latitude,
                article.longitude,
                article.altitude,
                article.street,
                article.street2,
                article.city,
                article.state,
                article.zip,
                article.country,
                article.phone,
                article.keywords,
                article.category,
                article.sourceName,
                article.sourceURL,
                article.language,
                toMySqlDateString(article.publishedDate),
                article.createdBy,
                toMySqlDateString(article.createdDate),
                article.modifiedBy,
                modDate)

            numberInserted = cursor.execute(self.lastSelect, valuesTuple)
            self.getConnection().commit()
            if (numberInserted < 1):
                raise DaoException('Did not get expected value (1 or 2) on Article insert: ' + str(numberInserted))
            articleID = cursor.lastrowid

            #print self.lastSelect + str(valuesTuple)

            if (article.id is None):
                article.id = articleID
            elif (article.newspageArticleId is None):
                # TODO: Possibly query for the right newspage_article_id here???
                raise DaoException('Existing article must be linked to newspage.')

            self.lastSelect = self.INSERT_NEWSPAGE_ARTICLE

            numberInserted = cursor.execute(self.lastSelect,
                (article.newspageArticleId,
                article.id,
                article.newspageName))
            self.getConnection().commit()

            attachmentDao = AttachmentDaoFactory.create(self.applicationID)
            try:
                for attachment in article.attachments:
                    attachmentDao.write(article.id, attachment)
            finally:
                attachmentDao.cleanUp()

            commentDao = CommentDaoFactory.create(self.applicationID)
            try:
                for comment in article.comments:
                    commentDao.write(article.id, comment)
            finally:
                commentDao.cleanUp()

            if (article.newspageArticleId is None):
                article.newspageArticleId = cursor.lastrowid

            if (numberInserted < 1):
                raise DaoException('Did not get expected value (1 or 2) on Newspage Article insert: ' + str(numberInserted))

        finally:
            self.releaseCursor()

        return articleID

    def delete(self, article):
        ''' Delete an article.  Deletes the attachments and comments on the article, too.

            return True if an article was deleted.
        '''
        deleted = False

        try:
            commentDao = CommentDaoFactory.create(self.applicationID)
            try:
                commentDao.deleteByArticleID(article.id)
            finally:
                commentDao.cleanUp()

            attachmentDao = AttachmentDaoFactory.create(self.applicationID)
            try:
                attachmentDao.deleteByArticleID(article.id)
            finally:
                attachmentDao.cleanUp()

            cursor = self.getCursor()
            numberDeleted = cursor.execute(self.DELETE_ARTICLE, (article.id,))
            self.getConnection().commit()
            deleted = (numberDeleted > 0)
        finally:
            self.releaseCursor()
        return deleted

    def deleteByNewspage(self, newspageName):
        ''' Delete all the articles in a Newspage. '''
        deleted = False

        try:
            articles = self.fetchAll(newspageName)

            commentDao = CommentDaoFactory.create(self.applicationID)
            try:
                for article in articles:
                    commentDao.deleteByArticleID(article.id)
            finally:
                commentDao.cleanUp()

            attachmentDao = AttachmentDaoFactory.create(self.applicationID)
            try:
                for article in articles:
                    attachmentDao.deleteByArticleID(article.id)
            finally:
                attachmentDao.cleanUp()

            cursor = self.getCursor()
            numberDeleted = cursor.execute(self.DELETE_ARTICLE_BY_NEWSPAGE, (newspageName,))
            self.getConnection().commit()
            deleted = (numberDeleted > 0)
        finally:
            self.releaseCursor()
        return deleted

    def expire(self, newspageName, days):
        ''' Set EXPIRED = True for all articles that are older than 'days' old.

            returns the number of articles deleted
        '''
        countExpired = 0
        articles = self.fetchAll(newspageName)
        for article in articles:
            if (article.isOld(days)):
                article.expired = True
                retval = self.write(article)

                if (retval != article.id):
                    raise DaoException('Did not write record ' + str(article.id) + '; got ' + str(retval))
                else:
                    art = self.fetchByID(article.id)
                    if (not art.expired):
                        raise DaoException('Article ' + str(article.id) + ' not properly expired')

                countExpired += 1

        return countExpired

    def search(self, newspageName, sortType, searchTerms, findAllTerms = False, caseSensitive = False, limit = 50):
        ''' Delete all articles that are older than 'days' old.

            searchTerms - a list of search terms
            sortType - the order in which to search the articles
            findAllTerms - 'and' the search terms
            caseSensitive - case sensitive search
            limit - limit the search results to at most the given number; set limit to 0 to search all articles

            returns a list of articles that contain the search terms, or an empty list if none
        '''

        if ((limit is None) or (limit < 0)):
            limit = 0

        foundArticles = list()
        articles = self.fetchSorted(newspageName, sortType, publishedOnly=True)

        for article in articles:
            if (article.search(searchTerms, findAllTerms, caseSensitive)):
                foundArticles += [article]
                if ((limit > 0) and (len(foundArticles) >= limit)):
                    break
        return foundArticles

    def countByNewspage(self, newspageName, countNotPublished = False):
        ''' Count the number of articles in the newspage.

            return the number counted
        '''
        count = 0

        try:
            cursor = self.getCursor()
            if (countNotPublished):
                self.lastSelect = self.SELECT_COUNT_NOT_PUBLISHED
            else:
                self.lastSelect = self.SELECT_COUNT_ALL
            retval = cursor.execute(self.lastSelect, (newspageName,))
            self.getConnection().commit()

            if (retval == 1):
                t = cursor.fetchone()
                count = t[0]
            elif (retval > 1):
                raise DaoException('Unexpectedly returned ' + str(retval) + ' results on select')
        finally:
            self.releaseCursor()

        return count

    def __fetchNewspageNames(self):
        ''' Get a list of newspage names.

            returns a list of string names
        '''
        names = list()

        try:
            cursor = self.getCursor()
            self.lastSelect = self.SELECT_NEWSPAGE_NAMES
            retval = cursor.execute(self.lastSelect)
            self.getConnection().commit()

            if (retval > 0):
                for item in cursor.fetchall():
                    names += [item[0]]
        finally:
            self.releaseCursor()

        return names

    def buildCountReport(self):
        ''' Build a report showing:

                newspageName, total articles, articles pending

            sorted by newapage name.

            returns a list of tuples (string, int, int)
        '''
        # TODO: Refactor to make this a dict

        data = list()

        names = self.__fetchNewspageNames()
        for name in names:
            countAll = self.countByNewspage(name)
            countNotPub = self.countByNewspage(name, True)
            data += [(name, countAll, countNotPub)]

        return data
