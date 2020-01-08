

#Imports
import xml.parsers.expat
from utils import verifyNotWhitespace
from util.text_utils import *

#parser declarations
def rememberKey(key = "", single = False, keys = {"currentKey":"", "duplicateKey":False}):
    if (key != ""):
        keys["currentKey"] = key
        keys["duplicateKey"] = single
    return keys

def checkDuplicate(key, keys = list()):
    check = False
    for k in keys:
        if (k == key):
            check = True
    if (not check):
        keys += [key]
    return check

class Property:
    ''' Use this object to return properties from the iterator.
        attrs should be a dict() object.
    '''

    def __init__(self):
        self.name = ''
        self.content = ''
        self.attrs = None

class PropertyDataParser:
    """A properties file parsing class used to load and process
xml files that can be considered application properties
files.  Properties files should have the following simple
form:

    <properties>
        <property1 attribute1="test" attribute2="test">value</property1>
        <property2 attribute1="test">value2</property2>
        <property2>value3</property2>
    </properties>

It is possible to retrieve and use the entire properties
dictionary from the parser, but methods to get the keys
and individual properties are available as well."""

    #Constructor
    def __init__(self, filename):
        """Initialze the class with a file name relative to the path of the root script."""
        self.localProps = dict()
        self.localAttrs = dict()
        self.inCdata = False
        self.cdata = ''
        try:
            f = file(filename)
            data = f.read()
            f.close()
            self.parse(data)
        except IOError:
            raise "IOError attempting to access:", filename

    def ProcessStartElement(self, name, attrs):
        # Skip the element if it's a <properties> element
        if (name == 'properties'):
            return

        # See if the name has been encountered before
        isDup = checkDuplicate(name, self.localProps.keys())
        rememberKey(name, isDup)

        #check for the attributes
        if (isDup):
            # If the last instance of this property had only one attribute,
            # convert the attribute to a list and add the new ones
            if (type(list()) != type(self.localAttrs[name])):
                self.localAttrs[name] = [self.localAttrs[name]]
            self.localAttrs[name] += [attrs]

        else:
            self.localAttrs[name] = attrs

    def ProcessCharData(self, data):
        if (self.inCdata):
            self.cdata += data
        else:
            if ((data.isspace() != True) & (len(data) != 0) & (rememberKey()["currentKey"] != "")):
                if (rememberKey()["duplicateKey"] == False):
                    self.localProps[rememberKey()["currentKey"]] = data
                else:
                    oldValue = self.localProps[rememberKey()["currentKey"]]
                    if (type(oldValue) != type(list())):
                        self.localProps[rememberKey()["currentKey"]] = [oldValue, data]
                    else:
                        self.localProps[rememberKey()["currentKey"]] += [data]

    def StartCdata(self):
        self.inCdata = True
        self.cdata = ''

    def EndCdata(self):
        self.inCdata = False
        if ((self.cdata.isspace() != True) & (len(self.cdata) != 0) & (rememberKey()["currentKey"] != "")):
            if (rememberKey()["duplicateKey"] == False):
                self.localProps[rememberKey()["currentKey"]] = self.cdata
            else:
                oldValue = self.localProps[rememberKey()["currentKey"]]
                if (type(oldValue) != type(list())):
                    self.localProps[rememberKey()["currentKey"]] = [oldValue, self.cdata]
                else:
                    self.localProps[rememberKey()["currentKey"]] += [self.cdata]

    #Parse the data into a properties dictionary
    def parse(self, data):

        propertyParser = xml.parsers.expat.ParserCreate()
        propertyParser.StartElementHandler = self.ProcessStartElement
        propertyParser.CharacterDataHandler = self.ProcessCharData
        propertyParser.StartCdataSectionHandler = self.StartCdata
        propertyParser.EndCdataSectionHandler = self.EndCdata

        propertyParser.Parse(data);
        return self.localProps

    #Return the dictionary if you want the whole thing
    def getProperties(self):
        return self.localProps

    #Return a particular property
    def hasProperty(self, name):
        return (name in self.localProps)

    #Return a particular property
    def getProperty(self, name):
        return self.localProps[name]

    #Return a particular property
    def getSafeProperty(self, name, val = ''):
        data = val
        if (name in self.localProps):
            data = self.localProps[name]
        return data

    #Return a particular property attributes
    def getPropertyAttrs(self, name):
        return self.localAttrs[name]

    #Return a particular property as a list, useful when you know that a
    #property is duplicated in a file.
    def getPropertyAsList(self, name):
        data = self.localProps[name]

        if (type(list()) != type(data)):
           data = [data]

        return data

    #Return a particular property's attributes as a list
    def getPropertyAttrsAsList(self, name):
        data = self.localAttrs[name]

        if (type(list()) != type(data)):
           data = [data]

        return data

    #get the keys for the properties dictionary
    def keys(self):
        return self.localProps.keys();

    def __iter__(self):
        self.index = 0
        return self

    def next(self):
        '''Returns a list object containing 0 or more Property objects.'''
        data = list()

        if (self.index == len(self.localProps)):
            raise StopIteration

        name = self.localProps.keys()[self.index]

        contentList = self.getPropertyAsList(name)
        attrList = self.getPropertyAttrsAsList(name)

        for i in range(len(contentList)):
            prop = Property()
            prop.name = name
            prop.content = contentList[i]
            prop.attrs = attrList[i]

            data += [prop]

        self.index += 1
        return data

class PropertyFileBuilder:

    def __init__(self):
        self.names = list()
        self.values = dict()
        self.attrs = dict()
        self.useCData = False

    def setCData(self, useCData):
        ''' Indicate that the property contents should be written with the CDATA element. '''
        self.useCData = useCData

    def add(self, name, value = None, attrs = None):
        ''' Add a property to the builder.

            name - the name of the property (the element name)
            value - the text data of the property; defaults to None
            attrs - k-v dictionary of attributes for this property; defaults to None
        '''
        self.names += [name]
        if (value != None):
            self.values[len(self.names) - 1] = value
        if (attrs != None):
            self.attrs[len(self.names) - 1] = attrs

    def build(self):
        ''' Build and return the XML for the property file. '''
        data = '<?xml version="1.0"?>\n'
        data += '<properties>\n'
        for i in range(0, len(self.names)):
            name = str(self.names[i])
            data += '\t<' + name

            if (i in self.attrs):
                adict = self.attrs[i]
                for item in adict.keys():
                    data += ' ' + item + '="' + toSafeXMLAttributeText(adict[item]) + '"'
            if (i in self.values):
                if (self.useCData):
                    data += '><![CDATA[' + str(self.values[i]) + ']]></' + name + '>\n'
                else:
                    data += '>' + str(self.values[i]) + '</' + name + '>\n'
            else:
                data += '/>\n'
        data += '</properties>'
        return data

    def write(self, filename):
        ''' Write the property file. '''

        # TODO: Implement a semaphore... maybe...

        # Build it first to make sure there are not problems building the string
        data = self.build()

        f = file(filename, 'w')
        f.write(data)
        f.flush()
        f.close()

