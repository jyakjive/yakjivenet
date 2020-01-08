
# imports
import os
import time
from util.fileutils import *
from stripper import AnchorFinder

# declarations

# definitons

# classes

class SitemapGenerator:
    ''' Generate a google sitemap object and put it in the right directory.

        Starts from index.html in the directory, unless given another start page.

        This class should not pick up anchors that contain '.PY', '?', '#', or '&'...
        which I don't even need to worry about if I focus on the HTML files in the
        directory only.

        A future addition would be to optionally use the ui.stripper.AnchorFinder to
        parse out all anchors from the HTML files that are found.
    '''

    skippedVals = ['.PY', '.py', '?', '#', '&']

    def __init__(self, directory = None, rootURL = None, startPage = None):
        ''' Constructor. '''

        if ((directory is None) or (rootURL is None)):
            raise Exception('Directory and rootURL cannot be None.')

        self.directory = directory
        if (self.directory[len(self.directory) - 1] != '/'):
            self.directory += '/'

        self.rootURL = rootURL
        if (self.rootURL[len(self.rootURL) - 1] != '/'):
            self.rootURL += '/'

        if (startPage is None):
            self.startPage = 'index.html'
        else:
            self.startPage = startPage

        self.anchorDict = dict()

    def __getPageFilename__(self, pageURL):
        ''' Get the html page name from the URL.
            Assumes we're looking at a simple URL... that is:

                http://www.something.com/somedir/somepage.html
        '''

        if (pageURL.find(self.rootURL) != 0):
            raise Exception('Expecting child page to be at or below parent URL.')

        data = pageURL[len(self.rootURL):]
        return data

    def __buildAnchorList__(self, directory, filename, fileURL = None):
        ''' Process the directory and get the sitemap.xml contents.
            Populates an internal dict, does not return.
        '''

        if (len(self.anchorDict) > 10000):
            raise Exception('Too many html pages found.')

        if (not fileExists(directory + filename)):
            raise Exception('Could not find file: ' + directory + filename + '  URL:' + fileURL)

        data = readTextFile(directory + filename)

        anchorFinder = AnchorFinder(self.rootURL, self.skippedVals)
        anchors = anchorFinder.process(data)

        if (fileURL is None):
            if ((self.rootURL + filename) not in self.anchorDict.keys()):
                self.anchorDict[self.rootURL + filename] = 1
        else:
            if (fileURL not in self.anchorDict.keys()):
                self.anchorDict[fileURL] = 1

        for item in anchors:
            childName = self.__getPageFilename__(item)

            # skip the self reference
            if (filename == childName):
                continue

            # if it's not already in the dict, follow it
            if (item not in self.anchorDict.keys()):
                self.__buildAnchorList__(self.directory, childName, item)
                self.anchorDict[item] = 1

    def __buildXML__(self):
        ''' Build the sitemap.xml.

            Raise an Exception if no anchors have been found.
        '''

        if (len(self.anchorDict) == 0):
            raise Exception('No anchors found in ' + self.rootURL + '.')

        data = '<?xml version="1.0" encoding="UTF-8"?>\n'
        data += '<urlset xmlns="http://www.google.com/schemas/sitemap/0.84">\n'

        for item in self.anchorDict.keys():

            data += '  <url>\n'
            data += '    <loc>' + item + '</loc>\n'
            timestr = time.strftime('%Y-%m-%d', time.gmtime(time.time()))
            data += '    <lastmod>' + timestr + '</lastmod>\n'
            # TODO: dynamically set this to daily or weekly based on site usage
            if (self.startPage in item):
                data += '    <changefreq>daily</changefreq>\n'
                data += '    <priority>1.0</priority>\n'
            else:
                data += '    <changefreq>weekly</changefreq>\n'
                data += '    <priority>0.5</priority>\n'
            data += '  </url>\n'

        data += '</urlset>'

        return data


    def writeSitemap(self, writeLocation = None):
        ''' Process the files in the directory.  Direct the sitemap.xml to be
            written to the new location, if desired, otherwise, writes to the
            same directory that is being searched.

            Currently bombs if more than 10K anchors are found.
        '''

        try:
            self.__buildAnchorList__(self.directory, self.startPage)
            xml = self.__buildXML__()

            writeTextFile(self.directory + 'sitemap.xml', xml)
        except Exception, e:
            log('Exception when trying to write sitemap.xml: ' + repr(e))

