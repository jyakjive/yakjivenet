# imports

from newscommunity.ncvars import *
from newscommunity.application import APPLICATION
from time import time, gmtime, strftime
from newspage_handler import NewsPage
from util.html_utils import createHelpLink
from article import *
from article_handler import *
from db.article_dao import *

# declarations
helpPageType = '''
<p>&nbsp;&nbsp;&nbsp;<b>Blog</b> - Blog-type newspages offer a comment box.
<p>&nbsp;&nbsp;&nbsp;<b>Articles</b> - Articles have a simple text format and may be followed by a link and include an image.
<p>&nbsp;&nbsp;&nbsp;<b>Long articles</b> - Long articles have their own text format and may be followed by a link and include an image.
<p>&nbsp;&nbsp;&nbsp;<b>Guestbook</b> - Guestbook newspages are populated only by comments from visitors to your site.
<p>&nbsp;&nbsp;&nbsp;<b>Letters</b> - Letters newspages define the first paragraph block differently from the remainder.
<p>&nbsp;&nbsp;&nbsp;<b>Links</b> - Links newspages are simple links with descriptive text.
'''

helpHeadlineType = '''
<p>&nbsp;&nbsp;&nbsp;<b>Headline only</b> - On the section web page, the first
several newspage items will be displayed by their title only.
<p>&nbsp;&nbsp;&nbsp;<b>Short text</b> - A snippet of the article content will be shown along with the title and date.
<p>&nbsp;&nbsp;&nbsp;<b>Long text</b> - A longer portion of the article will be shown along with the title and date.
<p>&nbsp;&nbsp;&nbsp;<b>Full text</b> - The full text of the first article in the page will be shown on the section web page.
'''

helpPageAttributes = '''
<p>The following attributes determine how your newspage behaves in the application and how it appears within your website.
<p><b>ID</b> - The Newspage ID is an alphanumeric unique key that is used to refer to the Newspage within the application.
<p><b>Title</b> - The title of the newspage is the primary display name of the newspage in the public part of the website.
<p><b>Subtitle</b> - The subtitle is displayed less prominently than the title in some parts of the website.
<p><b>Page Type</b> - The type of the newspage indicates what format the articles on the newspage will take.''' + \
createHelpLink('[More on Page Type]', '[more on Page Type]', helpPageType) + '''
<p><b>Headline Type</b> - This is the form that the first few articles take
when printed on the leader web page for the section.''' + \
createHelpLink('[More on Page Type]', '[more on Headline Type]', helpHeadlineType) + '''
<p><b>Section</b> - This indicates to which section of the site the newspage will be connected.
<p><b>Column</b> - Column indicates which column on the section web page this newspage will appear.
Sections are 2 or 3 columns.
<p><b>Order</b> - The order determines in which items will be printed first in each column on the section web page.
<p><b>Display Number</b> - The display number is the number of items from the newspage that are displayed on the main section.
Some Page Types have only 1 item from the newspage displayed on the section.
<p><b>Published</b> - If unchecked, the newspage will not be displayed, published, in the public site.
<p><b>Active</b> - If unchecked, the newspage will not be available to add new items.
<p><b>Items Expire</b> - Indicates that items will be deleted from the site after the given time.
Most pages should be set to 'Never.'  <em><b>Expired items are permanently deleted with no warning!!!!</b></em>
<p><b>Blog</b> - This indicates the newspage is owned by one of the site columnists (registered users).
<p><b>Sort Type</b> - YakJive.com allows you to sort articles in each newspage by a few different criterial.  You may want to
experiment with different sorting schemes for dictionary newspages, travellogs, or current events-type articles.
<p><b>Prompt comments</b> - This is the prompt that users will see to know to click on to 'sign guestbook',
    'post news', or 'report problem,' for example.
<p><b>Allow comments</b> - Whether or not the page allows users to add comments.  Always checked for blogs or blog-type pages.
'''

# definitions

def getLongColumnNames(sectionColumns):
    cDict = dict()
    if (sectionColumns == 3):
        cDict = {0:'Left column', 1:'Main column', 2:'Right column'}
    else:
        cDict = {0:'Secondary column', 1:'Main column', 2:'Unused column'}
    return cDict

def createBlankPage(page, applicationID = None):

    if ((applicationID is None) or (applicationID == '') or (applicationID < 1)):
        applicationID = APPLICATION.ID

    article = Article()
    article.publishedDate = datetime.datetime.today()
    article.createdDate = datetime.datetime.today()
    article.modifiedDate = datetime.datetime.today()
    article.newspageName = page.name
    if (page.pageType == PAGE_GUESTBOOK):
        article.content = 'Welcome to our guestbook.  Please feel free to drop a comment!'
    else:
        article.content = 'Welcome!  Start adding your own content at any time.'
    article.title = 'Welcome!'
    article.published = True
    article.createdBy = NC_ADMIN
    article.modifiedBy = NC_ADMIN
    article.category = page.name

    adao = ArticleDaoFactory.create(applicationID)
    try:
        adao.write(article)
    finally:
        adao.cleanUp()

def newspageDataFileExists(page):
    ''' Simple utility method to see if the newspage-data.xml file exists.'''
    fileName = APPLICATION.dataDirectory + page.name + '-data.xml'
    check = fileExists(fileName)
    return check