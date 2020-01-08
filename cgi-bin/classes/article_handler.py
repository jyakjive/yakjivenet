
from util.fileutils import Semaphore, fileExists, log
from newscommunity.application import APPLICATION, NEWSITEMLIST_DICT
from article_to_html import *
from article import *

import xml.parsers.expat

# Definitons
def loadNewsItemList(pageName, fileDir = APPLICATION.dataDirectory):
    '''Load a NewsItem list.  Return None if the file did not exist.'''

    #raise Exception('DEPRECATED')

    if (pageName not in NEWSITEMLIST_DICT):

        fileName = fileDir +  pageName + '-data.xml'
        sem = Semaphore(fileDir + pageName + '_')
        sem.put()
        newsItems = None
        if (fileExists(fileName)):
            try:
                #log('loadNewsItemList: loading data for ' + pageName)
                f = file(fileName)
                data = f.read()
                f.close()

                #log('loadNewsItemList: parsing data for ' + pageName)
                newsItems = NewsItemList("data/rss2_properties.xml", APPLICATION.attachURL)
                newsItems.parse(data)
                #log('loadNewsItemList: sorting data for ' + pageName)
                newsItems.sort()
                #log('loadNewsItemList: done handling data for ' + pageName)

            except Exception, e:
                sem.remove()
                raise str('Unexpected exception attempting to load: ' + fileName + ' ' + str(e))
        sem.remove()

        NEWSITEMLIST_DICT[pageName] = newsItems
    else:
        newsItems = NEWSITEMLIST_DICT[pageName]
    return newsItems

def writeNewsItemList(pageName, niList):

    #raise Exception('DEPRECATED')

    fileName = APPLICATION.dataDirectory + \
        pageName + '-data.xml'
    sem = Semaphore(APPLICATION.newsFileLocation + pageName + '_')
    sem.put()

    try:
        nwslst = itemListToNewsItemListXML(niList)

        #Parse the XML to make sure it works ok
        newsItemParser = xml.parsers.expat.ParserCreate()
        newsItemParser.Parse(nwslst)

        #Write the new news item to the appropriate file
        f = file(fileName, 'w')
        f.write(nwslst)
        f.flush()
        f.close()
    except:
        sem.remove()
        raise
    sem.remove()
