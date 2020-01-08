
# imports
from newscommunity.application import APPLICATION
from newscommunity.ncvars import *
from utils import ConnectionAwareObject
from util.fileutils import *
import datetime
from classes.newspage_handler import *
from classes.article_handler import *
from classes.article import NewsItemList

from article_dao import *
from attachment_dao import *
from comment_dao import *

# declarations

# definitions

# classes

class SiteDbCreator:
    ''' This class is used to create the new database tables for a new YakJive site.'''

    def __init__(self, siteID):
        self.siteID = siteID

        self.sqlDir = 'data/sql/'

        self.sqlFiles = [
            'create_table_category.sql',
            'create_table_classification.sql',
            'create_table_article.sql',
            'create_table_attachment.sql',
            'create_table_comment.sql',
            'create_table_article_attachment.sql',
            'create_table_newspage_article.sql']

        self.sqlDrop = 'drop_tables.sql'

    def execute(self):
        ''' Do the table creation. '''
        sql = list()

        for item in self.sqlFiles:
            data = readTextFile(self.sqlDir + item, replaceDict={'ID': str(self.siteID)})
            sql += [data.replace('\n', '')]

        cao = ConnectionAwareObject()
        for item in sql:
            #print item
            data = cao.executePassthroughQuery(item)

            #print str(data)

    def cleanUp(self, hideErrors = True):
        ''' Clean up the table creates. '''
        data = readTextFile(self.sqlDir + self.sqlDrop, replaceDict={'ID': str(self.siteID)})
        sql = data.split('\n')

        cao = ConnectionAwareObject()
        for item in sql:
            #print item
            try:
                data = cao.executePassthroughQuery(item)
            except Exception, e:
                if (not hideErrors):
                    raise e

    def migrate(self, siteCgiPath, count = None, startAt = None):
        ''' Migrate old style site articles into the database.

            siteID - the integer id of the site to be migrated
            siteCgiPath - the url to the site, such as ../cgi-bin/yj/testsite
        '''

        #log('Entering SiteDbCreator.migrate()')

        data = ''

        # Load the newspage properties
        npfilename = siteCgiPath + FILENAME_PAGES
        newspages = loadNewsPageProperties(npfilename)

        # for each newspage load the articles and push them into the db
        articles = list()
        lasttotal = 0
        for pagename in newspages:
            page = newspages[pagename]

            # Load the articles
            newsitems = loadNewsItemList(page.name, siteCgiPath + 'data/newsItems/')

            if (newsitems is None):
                continue

            #log('Loaded news items for ' + page.name)

            for item in newsitems.items:
                article = Article()
                article.id = None
                article.title = item.title
                article.content = item.content
                article.hideAddress = item.hideAddress
                article.published = item.isVisible
                article.expired = False
                article.latitude = item.latitude
                article.longitude = item.longitude
                article.altitude = item.altitude
                article.street = item.street
                article.street2 = item.street2
                article.city = item.city
                article.state = item.state
                article.zip = item.zip
                article.country = item.country
                article.phone = item.phone
                article.keywords = item.category
                article.category = item.category
                article.sourceName = item.sourceName
                article.sourceURL = item.sourceURL
                article.publishedDate = \
                    datetime.datetime(int(item.year), int(item.month), int(item.day), int(item.hour), int(item.minute))
                article.createdBy = item.nickname
                try:
                    if (int(item.lmYear) == 0):
                        raise Exception('bad to use exceptions for flow control, but...')
                    else:
                        theDate = datetime.datetime(int(item.lmYear), int(item.lmMonth), int(item.lmDay), int(item.lmHour), int(item.lmMinute))
                except:
                    theDate = datetime.datetime.today()
                article.createdDate = theDate
                article.modifiedBy = item.modifiedBy
                article.modifiedDate = theDate

                article.newspageArticleId = None
                article.newspageName = page.name

                for iattachment in item.attachments:
                    attachment = Attachment()
                    attachment.id = None
                    attachment.filename = iattachment.name
                    attachment.originalFilename = iattachment.origName
                    attachment.notes = iattachment.notes
                    attachment.align = iattachment.align
                    attachment.image = iattachment.isImg
                    attachment.imageHeight = iattachment.imgHeight
                    attachment.imageWidth = iattachment.imgWidth
                    attachment.thumbnailName = None
                    attachment.thumbnailHeight = 0
                    attachment.thumbnailWidth = 0
                    attachment.size = iattachment.size
                    attachment.createdDate = datetime.datetime.today()
                    article.attachments += [attachment]

                for icomment in item.comments:
                    comment = Comment()
                    comment.id = None
                    comment.content = icomment.text
                    comment.name = icomment.name
                    comment.email = icomment.email
                    comment.hideAddress = icomment.hideAddress
                    theDate = datetime.datetime.today()
                    try:
                        if (icomment.month == 'Jan'): icomment.month = '1'
                        if (icomment.month == 'Feb'): icomment.month = '2'
                        if (icomment.month == 'Mar'): icomment.month = '3'
                        if (icomment.month == 'Apr'): icomment.month = '4'
                        if (icomment.month == 'May'): icomment.month = '5'
                        if (icomment.month == 'Jun'): icomment.month = '6'
                        if (icomment.month == 'Jul'): icomment.month = '7'
                        if (icomment.month == 'Aug'): icomment.month = '8'
                        if (icomment.month == 'Sep'): icomment.month = '9'
                        if (icomment.month == 'Oct'): icomment.month = '10'
                        if (icomment.month == 'Nov'): icomment.month = '11'
                        if (icomment.month == 'Dec'): icomment.month = '12'
                        theDate = datetime.datetime(int(icomment.year), int(icomment.month), int(icomment.day))
                    except Exception, e:
                        log('Exception creating comment date: ' + repr(e))
                    comment.createdDate = theDate
                    article.comments += [comment]

                articles += [article]

            data +=  'Found ' + str(len(articles) - lasttotal) + ' articles in newspage ' + page.name + '<BR>\n'
            #print  'Found ' + str(len(articles) - lasttotal) + ' articles in newspage ' + page.name + '<BR>\n'
            lasttotal = len(articles)

        #log('Found ' + str(len(articles)) + ' articles')

        dao = ArticleDaoFactory.create(self.siteID)
        counter = 0
        try:
            for arts in articles:
                if ((count is not None) and (startAt is not None) and (counter - startAt < 0)):
                    counter += 1
                    continue
                elif ((count is not None) and (startAt is not None) and (counter - startAt >= count)):
                    break
                try:
                    aid = dao.write(arts)
                    #log('Successfully inserted article ' + arts.newspageName + '.' + arts.title)
                except Exception, e:
                    log('Failed on insert article ' + arts.newspageName + '.' + arts.title + ' ' + str(e))
                    data += 'Failed on insert: ' + str(arts.newspageName) + '.' + str(arts.title) + ' ' + str(e) + '<BR>\n'
                    #print 'Failed on insert: ' + str(arts.newspageName) + '.' + str(arts.title) + ' ' + str(e) + '<BR>\n'
                counter += 1
        finally:
            dao.cleanUp()

        data += 'Stopped at number: ' + str(counter)

        return data
