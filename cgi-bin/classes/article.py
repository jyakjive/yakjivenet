#Imports
import string
import xml.parsers.expat
from time import *
from util.utils import remember
import util.properties
from util.image_utils import *
from newscommunity.ncvars import *
from util.text_utils import *
from util.html_utils import *
import re

#Declarations
remember('currentItem', None)
remember('currentProperty', None)
remember('newsItems', [])

longTimeFormat = '%a, %d %b %Y %H:%M:%S %Z'

# Definitons


# TODO-L: Figure out where this should go
def generateRSSName(domain, page, urlroot):
    data = urlroot
    data += domain.replace('.', '-')
    data += '-' + page + '-rss.xml'
    return data

#Classes

class RSSTemplate:
    '''This class loads the rss properties and uses them to format the
    rss xml file.'''

    #title = ''
    #link = ''
    #description = ''
    #language = ''
    #pubDate = ''
    #managingEditor = ''
    #webMaster = ''
    #copyright = ''

    def __init__(self, filename):
       rssPropParser = util.properties.PropertyDataParser(filename)
       self.title = rssPropParser.getSafeProperty('title', '')
       self.link = rssPropParser.getSafeProperty('link', '')
       self.description = rssPropParser.getSafeProperty('description', '')
       self.language = rssPropParser.getSafeProperty('language', '')
       self.managingEditor = rssPropParser.getSafeProperty('managingEditor', '')
       self.webMaster = rssPropParser.getSafeProperty('webMaster', '')
       self.copyright = rssPropParser.getSafeProperty('copyright', '')
       self.pubDate = strftime(longTimeFormat, gmtime())

    def getHeader(self):
        data = ''
        data += '<?xml version="1.0"?>\n'
        data += '<rss version="2.0">\n'
        data += '   <channel>\n'
        data += '      <title>' + self.title + '</title>\n'
        data += '      <link>' + self.link + '</link>\n'
        data += '      <description>' + self.description + '</description>\n'
        data += '      <language>' + self.language + '</language>\n'
        data += '      <pubDate>' + self.pubDate + '</pubDate>\n'
        data += '      <managingEditor>' + self.managingEditor + '</managingEditor>\n'
        data += '     <webMaster>' + self.webMaster + '</webMaster>\n'
        data += '      <copyright>' + self.copyright + '</copyright>\n'
        return str(data)

    def getFooter(self):
        data = ''
        data += '   </channel>\n'
        data += '</rss>\n'
        return str(data)

class NewsItemList:
    '''A collection of news items'''

    def __init__(self, filename = 'RSS filename not set', imageUrl = '/uploads'):
        #raise Exception('DEPRECATED')

        self.items = []
        self.currentItem = None
        self.currentProperty = ''
        self.isSorted = False
        self.rssFileName = filename
        #TODO-R: Consider refactoring out imageUrl
        self.imageUrl = imageUrl
        self.sortType = SORT_DATE

    def count(self, countVisibleOnly = False):
        data = 0
        if (self.items is not None):
            if (not countVisibleOnly):
               data = len(self.items)
            else:
                for item in self.items:
                    if (item.isVisible):
                        data += 1
        return data

    def add(self, item):
        '''Adds an item to the list and gives it a new unique id
        if it doesn't have one already.'''
        if (item.uid <= 0):
            luid = self.getMaxId() + 1
            item.uid = luid
        self.items += [item]
        self.isSorted = False

    def find(self, tuid):
        '''Finds the item that matches the unique id'''
        item = None
        tuid = int(tuid)
        for itm in self.items:
           if (itm.uid == tuid):
              item = itm
              break
        return item

    def getRank(self, tuid):
        ''' Get the position of the article in the list, starts at zero. '''
        self.sort()
        data = -1
        for i in range(len(self.items)):
            if (tuid == self.items[i].uid):
                data = i
                break
        return data

    def getVisibleItems(self, quantity = 1):
        titems = list()
        counter = 0
        for item in self.items:
            if (item.isVisible):
                counter += 1
                titems += [item]
            if (counter == quantity):
                break
        return titems

    def remove(self, item):
        '''Removes items using the item's unique id.  Helps reinforce
        that there should be no duplicate ids.'''
        rmlist = []
        for itm in self.items:
            if (item.uid == itm.uid):
               rmlist += [itm]
        for rmi in rmlist:
            self.items.remove(rmi)
        self.isSorted = False

    def setSortType(self, sortType):
        if (sortType != self.sortType):
            self.sortType = sortType
            self.isSorted = False
        self.sort()

    def sort(self):
        if ((not self.isSorted) & (len(self.items) > 1)):
            if (self.sortType == SORT_ALPHABETIC):
                self.sortAlphabetic()
            elif (self.sortType in [SORT_DATE_REVERSE, SORT_DATE_REVERSE_LM]):
                self.sortDateReverse()
            else: #SORT_DATE, SORT_DATE_LM
                self.sortDate()

    def sortDateReverse(self):
        '''Sorts the news items in order from oldest to newest'''
        a = self.items
        displayDate = (self.sortType == SORT_DATE_REVERSE)
        for i in range(len(a) - 1):
            for j in range(i + 1, len(a)):
                if (a[i].getDateAsInt(displayDate) > a[j].getDateAsInt(displayDate)):
                   t = a[j]
                   a[j] = a[i]
                   a[i] = t
        self.items = a
        self.isSorted = True

    def sortDate(self):
        '''Sorts the news items in order from newest to oldest'''
        a = self.items
        displayDate = (self.sortType == SORT_DATE)
        for i in range(len(a) - 1):
            for j in range(i + 1, len(a)):
                if (a[i].getDateAsInt(displayDate) < a[j].getDateAsInt(displayDate)):
                   t = a[j]
                   a[j] = a[i]
                   a[i] = t
        self.items = a
        self.isSorted = True

    def sortAlphabetic(self):
        # Use the comparability of strings to do this sort
        a = self.items

        for i in range(len(a) - 1):
            for j in range(i + 1, len(a)):
                # NOTE: Could refactor to use cmp(x.lower(),y.lower())
                if (a[i].title.lower() > a[j].title.lower()):
                   t = a[j]
                   a[j] = a[i]
                   a[i] = t
                elif (a[i].title.lower() == a[j].title.lower()):
                    if (a[i].getDateAsInt() < a[j].getDateAsInt()):
                       t = a[j]
                       a[j] = a[i]
                       a[i] = t
        self.items = a
        self.sorted = True

    def getMaxId(self):
        '''Get the current highest id in the list'''
        val = -1
        if (len(self.items) > 0):
           for item in self.items:
               if (item.uid > val):
                   val = item.uid
        return val

    def getItems(self):
        """Get the list of items."""
        return self.items

    def getItem(self, index):
        """Get an item by it's current index in the list."""
        return self.items[index]

    def getByUid(self, uid):
        """Get an item by it's uid."""
        data = None
        for item in self.items:
            if (item.uid == uid):
                data = item
                break
        return data

    def expire(self, days):
        '''Remove any items that are older than the number of days.'''

        ind = 0

        while (ind < len(self.items)):
            if (self.items[ind].isOld(days)):
                del self.items[ind]
            else:
                ind += 1

    def search(self, searchTerms, findAllTerms = False, caseSensitive = False):
        '''Search the articles for a given search term or terms.
            searchTerms - a list of search terms
            returns a list of UID's for articles that matched'''

        matches = list()

        for item in self.items:
            if (item.search(searchTerms, findAllTerms, caseSensitive)):
                matches += [item.uid]

        return matches

    def getFirstSorted(self, sortType = SORT_DATE):
        ''' Internal utility method that sorts the items, then returns
           the date of the first, then sorts them back.
           returns a (day, month, year) tuple or None if there are no items. '''
        data = None
        oldSortType = self.sortType
        self.setSortType(sortType) # does the sort if there was a change
        if (len(self.items) > 0):
            data = self.items[0].day, self.items[0].month, self.items[0].year
        self.setSortType(oldSortType)
        return data

    def __processNewsItemElement__(self, name, attrs):
        if (name == 'NewsItem'):
            self.currentItem = NewsItem()
        elif (name == 'attachment'):
            self.currentItem.addAttachment( \
                attrs['name'], \
                attrs['origName'], \
                attrs['notes'], \
                attrs['align'], \
                (attrs['isImg'] in TRUE), \
                attrs['imgHeight'], \
                attrs['imgWidth'], \
                attrs['size'])
        elif (name == 'comment'):
            #if (self.currentItem is None):
            #    self.currentItem = NewsItem()
            hideAddress = True
            try:
                hideAddress = (attrs['hideAddress'] in TRUE)
            except:
                hideAddress = True
            if ('id' in attrs):
                cid = int(attrs['id'])
            else:
                cid = -1;
            self.currentItem.addComment( \
                attrs['text'], \
                attrs['day'], \
                attrs['month'], \
                attrs['year'], \
                attrs['email'], \
                attrs['name'], \
                str(hideAddress), \
                cid)
        else:
            self.currentProperty = name

    def __processNewsItemElementEnd__(self, name):
        if (name == 'NewsItem'):
            self.items += [self.currentItem]
            #self.currentItem = None

    def __processNewsItemCharData__(self, data):
        if ((data.isspace() != True) and (len(data) != 0)):
            if (self.currentItem <> None):
                if (self.currentProperty == 'UniqueID'):
                    self.currentItem.uid = int(data)
                elif (self.currentProperty == 'Title'):
                    self.currentItem.title = str(safeText(data))
                elif (self.currentProperty == 'SourceName'):
                    self.currentItem.sourceName = str(data)
                elif (self.currentProperty == 'SourceURL'):
                    self.currentItem.sourceURL = str(data)
                elif (self.currentProperty == 'Category'):
                    self.currentItem.category = str(data)
                elif (self.currentProperty == 'Content'):
                    self.currentItem.content += safeText(unicode(data))
                elif (self.currentProperty == 'Nickname'):
                    self.currentItem.nickname += str(data)
                elif (self.currentProperty == 'ModifiedBy'):
                    self.currentItem.modifiedBy += str(data)
                elif (self.currentProperty == 'HideAddress'):
                    self.currentItem.hideAddress = (data in TRUE)
                elif (self.currentProperty == 'IsVisible'):
                    self.currentItem.isVisible = (data in TRUE)
                elif (self.currentProperty in ['Date', 'LastModified']):
                    try:
                        # Use these lines for Py2.3-4
                        data = data.replace('EST', 'Mountain Standard Time')
                        tdata = strptime(data, longTimeFormat)
                    except:
                        # Use these lines for Py2.2
                        # TODO-L: Make sure that I want to trim so much from the date
                        if (data.find('Mountain') > -1):
                            ttdata = data[0:(data.find('Mountain'))]
                            ttdata = data[0: len(ttdata) - 4]
                            tdata = strptime(ttdata, longTimeFormat[0:(len(longTimeFormat) - 6)])
                        else:
                            try:
                                data = data.strip()
                                tdata = strptime(data[0:(len(data) - 3)], longTimeFormat[0:(len(longTimeFormat) - 3)])
                            except Exception, e:
                                # backward compatibility to the old style sites with no seconds
                                tdata = strptime(data[0:(len(data) - 3)], longTimeFormat[0:(len(longTimeFormat) - 6)])
                    if (self.currentProperty == 'Date'):
                        self.currentItem.month = str(strftime('%m', tdata))
                        self.currentItem.day = str(strftime('%d', tdata))
                        self.currentItem.year = str(strftime('%Y', tdata))
                        self.currentItem.hour = str(strftime('%H', tdata))
                        self.currentItem.minute = str(strftime('%M', tdata))
                    else:
                        self.currentItem.lmMonth = str(strftime('%m', tdata))
                        self.currentItem.lmDay = str(strftime('%d', tdata))
                        self.currentItem.lmYear = str(strftime('%Y', tdata))
                        self.currentItem.lmHour = str(strftime('%H', tdata))
                        self.currentItem.lmMinute = str(strftime('%M', tdata))
                elif (self.currentProperty in ['longitude', 'latitude', 'altitude']):
                    self.currentItem.__dict__[self.currentProperty] = float(data)
                elif (self.currentProperty in ['street', 'street2', 'city', 'state', 'zip', 'country', 'phone']):
                    self.currentItem.__dict__[self.currentProperty] = str(data)

    def parse(self, data):
        newsItemParser = xml.parsers.expat.ParserCreate()
        newsItemParser.StartElementHandler = self.__processNewsItemElement__
        newsItemParser.EndElementHandler = self.__processNewsItemElementEnd__
        newsItemParser.CharacterDataHandler = self.__processNewsItemCharData__
        newsItemParser.Parse(data)
        self.sort()

class Comment:
    '''Capture the information necessary for a guestbook or feedback on a blog.'''

    def __init__(self):
        #raise Exception('DEPRECATED')
        self.text = ''
        self.month = ''
        self.day = ''
        self.year = ''
        self.email = ''
        self.name = ''
        self.hideAddress = True
        self.id = 0

    def toXML(self):
        data = '<comment '
        data += ' text="' + toSafeXMLAttributeText(self.text) + '"'
        data += ' month="' + str(self.month) + '"'
        data += ' day="' + str(self.day) + '"'
        data += ' year="' + str(self.year) + '"'
        data += ' email="' + toSafeXMLAttributeText(self.email) + '"'
        data += ' name="' + toSafeXMLAttributeText(self.name) + '"'
        data += ' id="' + str(self.id) + '"'
        data += ' hideAddress="' + str(self.hideAddress) + '"'
        data += '/>'
        return data

class Attachment:
    '''Capture the information necessary for an attachment to a news item.'''

    def __init__(self):
        #raise Exception('DEPRECATED')
        self.name = ''
        self.origName = ''
        self.notes = ''
        self.align = ''
        self.isImg = False
        self.imgHeight = 0
        self.imgWidth = 0
        self.size = 0

    def toXML(self):
        data = '<attachment '
        data += ' name="' + str(self.name) + '"'
        data += ' origName="' + str(self.origName) + '"'
        data += ' notes="' + toSafeXMLAttributeText(self.notes) + '"'
        data += ' align="' + str(self.align) + '"'
        if (self.isImg):
            data += ' isImg="True"'
        else:
            data += ' isImg="False"'
        data += ' imgHeight="' + str(self.imgHeight) + '"'
        data += ' imgWidth="' + str(self.imgWidth) + '"'
        data += ' size="' + str(self.size) + '"'
        data += '/>'
        return data

class NewsItem:
    '''The NewsItem class encapsulates the data and operations
    that make up a NewsItem while the data are in memory.  The
    class contains methods for generating XML, RSS feeds, and
    HTML.'''

    def __init__(self):
        #raise Exception('DEPRECATED')

        self.title = ''
        self.year = ''
        self.month = ''
        self.day = ''
        self.hour = '0'
        self.minute = '0'
        self.lmYear = ''
        self.lmMonth = ''
        self.lmDay = ''
        self.lmHour = '0'
        self.lmMinute = '0'
        self.sourceName = ''
        self.sourceURL = ''
        self.category = ''
        self.content = ''
        self.uid = 0
        self.nickname = ''
        self.modifiedBy = ''
        self.imgHeight = 0
        self.imgWidth = 0
        self.isImg = False
        self.comments = list()
        self.attachments = list()
        self.hideAddress = False
        self.isVisible = True

        self.longitude = None
        self.latitude = None
        self.altitude = None

        self.street = None
        self.street2 = None
        self.city = None
        self.state = None
        self.zip = None
        self.country = None
        self.phone = None

        # Internal vars
        self.dateInt = None
        self.lmDateInt = None

    def search(self, searchTerms, findAllTerms = False, caseSensitive = False):
        '''Search the article for a given search term or terms.
            searchTerms - a list of search terms. '''

        check = self.isVisible

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
                # TODO: Should this be '+=' or just '=' ???
                terms = [tmp]

            for term in terms:
                if (caseSensitive):
                    check2 = ((re.search(term, self.title) is not None) or \
                        (re.search(term, self.content) is not None) or \
                        (re.search(term, self.category) is not None) or \
                        (re.search(term, self.sourceName) is not None) or \
                        (re.search(term, self.sourceURL) is not None) or \
                        (re.search(term, self.nickname) is not None))
                else:
                    term = term.lower()
                    check2 = ((re.search(term, self.title.lower()) is not None) or \
                        (re.search(term, self.content.lower()) is not None) or \
                        (re.search(term, self.category.lower()) is not None) or \
                        (re.search(term, self.sourceName.lower()) is not None) or \
                        (re.search(term, self.sourceURL.lower()) is not None) or \
                        (re.search(term, self.nickname.lower()) is not None))

                check = check and check2

        return check

    def setDate(self, year, month, day):
        now = gmtime()
        self.year = year
        self.month = month
        self.day = day

        if ((int(year) == now[0]) and \
                (int(month) == now[1]) and \
                (int(day) == now[2])):
            self.hour = str(now[3])
            self.minute = str(now[4])

    def addComment(self, comment = None, day = None, month = None, year = None, \
            email = None, name = None, hideAddress = 'True', tcid = -1):
        cid = 0
        if (tcid == -1):
            for item in self.comments:
                if (item.id > cid):
                    cid = item.id
            cid += 1
        else:
            cid = tcid

        if (type(comment) == type(Comment())):
            comment.id = cid
            comments += [comment]
        elif (comment is not None):
            c = Comment()
            c.text = undoSafeHTML(comment)
            c.day = day
            c.month = month
            c.year = year
            c.email = undoSafeHTML(email)
            c.name = undoSafeHTML(name)
            c.hideAddress = (hideAddress in TRUE)
            c.id = cid
            self.comments += [c]

    def addAttachment(self, name, origName = None, notes = None, align = None, \
        isImg = None, imgHeight = None, imgWidth = None, size = None):

        if (type(name) == type(Attachment())):
            self.attachments += [name]
        else:
            a = Attachment()
            a.name = name
            a.origName = origName
            a.notes = undoSafeHTML(notes)
            a.align = align
            a.isImg = isImg
            a.imgHeight = imgHeight
            a.imgWidth = imgWidth
            a.size = size
            self.attachments += [a]

    def getSimpleDateString(self, displayDate = True):
        ''' Get the display date as a simple date string
            "June 14, 2005 13:03"
            If displayDate == False, then this will return the XML date
            for the last-modified date.
        '''
        data = ''
        # Extra checks are for legacy data with no LM date
        if (displayDate or (self.lmYear == '') or (self.lmYear is None)):
            data = self.month + ' ' + self.day + ' ' + self.year + \
                ' ' + self.hour + ':' + self.minute
        else:
            data = self.lmMonth + ' ' + self.lmDay + ' ' + self.lmYear + \
                ' ' + self.lmHour + ':' + self.lmMinute
        if (data != ''):
            tdata = strptime(data, '%m %d %Y %H:%M')
            data = strftime('%B %d, %Y %H:%M', tdata)
        return str(data)

    def getXMLDateString(self, displayDate = True):
        ''' Get an XML Date string to be used in the written out files.
            If displayDate == False, then this will return the XML date
            for the last-modified date.
        '''
        data = ''
        # Extra checks are for legacy data with no LM date
        if (displayDate or (self.lmYear == '') or (self.lmYear is None)):
            data = self.month + ' ' + self.day + ' ' + self.year + \
                ' ' + self.hour + ':' + self.minute
        else:
            # Last modified date
            # TODO-R: Refactor to eliminate the empty string check when we are not using legacy xml anymore
            if (self.lmYear != ''):
                data = self.lmMonth + ' ' + self.lmDay + ' ' + self.lmYear + \
                    ' ' + self.lmHour + ':' + self.lmMinute
        if (data != ''):
            tdata = strptime(data, '%m %d %Y %H:%M')
            data = strftime(longTimeFormat, tdata)
            #Tue, 03 Jun 2003 09:39:21 GMT
        return str(data)

    def __getDateAsInt__(self, year, month, day, hour, minute):
        data = 0
        if ((year is not None) and (year != '')):
            data = month + ' ' + day + ' ' + year + ' ' + hour + ':' + minute
            data = strptime(data, '%m %d %Y %H:%M')
            data = mktime(data)
        return data

    def getDateAsInt(self, displayDate = True):
        '''Get the display date as an int of seconds.
            If displayDate == False, then this will return the XML date
            for the last-modified date.

            This stuff is contorted because I added in the LastModified date late.
        '''

        data = 0
        if (displayDate):
            self.dateInt = self.__getDateAsInt__(self.year, self.month, self.day, self.hour, self.minute)
            data = self.dateInt
        else:
            if ((self.lmYear is not None) and (self.lmYear != '')):
                self.lmDateInt = self.__getDateAsInt__(self.lmYear, self.lmMonth, self.lmDay, self.lmHour, self.lmMinute)
            else:
                self.lmDateInt = self.__getDateAsInt__(self.year, self.month, self.day, self.hour, self.minute)
            data = self.lmDateInt
        return data

    def getDateAsInt2(self):
        '''Get the display date as an int of days, but leave out the time.'''
        if (self.dateInt is None):
            data = self.month + ' ' + self.day + ' ' + self.year
            tdata = strptime(data, '%m %d %Y')
            data = mktime(tdata)
            self.dateInt = int(float(data) / 3600.0 / 24.0)
        return self.dateInt

    def isOld(self, days, displayDate = True):
        '''Check to see if the item's display date (or last-modified
            date if displayDate == False is older than 'days' old.
        '''
        curtime = mktime(gmtime(time.time()))
        itemtime = None
        if (displayDate):
            itemtime = self.getDateAsInt()
        else:
            itemtime = self.getDateAsInt(False)
        timedif = curtime - itemtime
        timedif = timedif / 60.0 / 60.0 / 24.0
        return (timedif > days)

    def toXML(self):
        xml = '  <NewsItem>\n'
        xml += '    <Title><![CDATA[' + str(safeText(self.title)) + ']]></Title>\n'
        xml += '    <Date>' + self.getXMLDateString() + '</Date>\n'
        if ((self.lmYear is not None) and (self.lmYear != '')):
            xml += '    <LastModified>' + self.getXMLDateString(False) + '</LastModified>\n'
        xml += '    <Category><![CDATA[' + safeText(self.category) + ']]></Category>\n'
        xml += '    <SourceName><![CDATA[' + safeText(self.sourceName) + ']]></SourceName>\n'
        xml += '    <SourceURL><![CDATA[' + safeText(self.sourceURL) + ']]></SourceURL>\n'
        xml += '    <Content><![CDATA[' + safeText(self.content) + ']]></Content>\n'
        xml += '    <UniqueID>' + str(self.uid) + '</UniqueID>\n'
        xml += '    <Nickname><![CDATA[' + str(self.nickname) + ']]></Nickname>\n'
        xml += '    <ModifiedBy><![CDATA[' + str(self.modifiedBy) + ']]></ModifiedBy>\n'
        xml += '    <HideAddress><![CDATA[' + str(self.hideAddress) + ']]></HideAddress>\n'
        if (self.isVisible):
            xml += '    <IsVisible>True</IsVisible>\n'
        else:
            xml += '    <IsVisible>False</IsVisible>\n'

        # add location elements
        for item in ['longitude', 'latitude', 'altitude']:
            if (self.__dict__[item] is not None):
                xml += '    <' + item + '><![CDATA[' + repr(self.__dict__[item]) + ']]></' + item + '>\n'

        for item in ['street', 'street2', 'city', 'state', 'zip', 'country', 'phone']:
            if (self.__dict__[item] is not None):
                xml += '    <' + item + '><![CDATA[' + str(self.__dict__[item]) + ']]></' + item + '>\n'

        for item in self.attachments:
            xml += '\t' + item.toXML() + '\n'
        for item in self.comments:
            xml += '\t' + item.toXML() + '\n'
        xml += '  </NewsItem>\n'
        return str(xml)
