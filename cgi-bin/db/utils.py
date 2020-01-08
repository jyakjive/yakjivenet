
# imports
from newscommunity.application import APPLICATION
import MySQLdb
import datetime
import time
from newscommunity.ncvars import TRUE
from util.fileutils import log

# declarations

# definitions
def toMySqlDateString(adate):
    ''' Converts to a simple string format for inserting into a MySQL database DATETIME field. '''
    data = ''
    if (type(adate) == type(time.time())):
        data = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(adate))
    elif (type(adate) == type(datetime.datetime.now())):
        data = adate.strftime('%Y-%m-%d %H:%M:%S')
    else:
        raise Exception('db.utils.toMySqlDateString(): Got unexpected date type [' + str(adate) + ':' + str(type(adate)) + ']')
    return data

def safeMySqlEscapeString(astring):
    ''' Returns None if the string is None, otherwise returns the escaped string. '''
    data = astring
    if (data is not None):
        data = str(data)
        data = MySQLdb.escape_string(data)
    return data

def toMySqlBoolean(flag):
    ''' Returns 1 or 0 for True or False. '''
    data = 0
    if (flag in TRUE):
        data = 1
    return data

# classes
class ConnectionAwareObject:
    ''' Base class for classes that need to use a database connection. '''

    __db = None
    __cursor = None

    # Utility var used by inherited objects sometimes...
    lastSelect = ''

    def __init__(self):
        if ('cursorCount' not in ConnectionAwareObject.__dict__):
            ConnectionAwareObject.__dict__['cursorCount'] = 0
        if ('connectionCount' not in ConnectionAwareObject.__dict__):
            ConnectionAwareObject.__dict__['connectionCount'] = 0

    def getConnection(self):
        return self.__db

    def getCursor(self):
        if (self.__cursor is None):
            if (self.__db is None):
                self.__db=MySQLdb.connect(user=APPLICATION.dbUser,passwd=APPLICATION.dbPassword,db=APPLICATION.db)
                ConnectionAwareObject.__dict__['connectionCount'] += 1
            self.__cursor = self.__db.cursor()
            ConnectionAwareObject.__dict__['cursorCount'] += 1
        return self.__cursor

    def releaseCursor(self):
        if (self.__cursor is not None):
            self.__cursor.close()
            self.__cursor = None

    def cleanUp(self):
        ''' This method should be called whenever you are done with a ConnectionAwareObject. '''
        if (self.__db is not None):
            self.__db.close()
            self.__db = None

    def executePassthroughQuery(self, query):
        ''' Execute a passthrough query and return all the results as a list of tuples. '''
        data = list()
        try:
            cursor = self.getCursor()

            self.lastSelect = query
            retval = cursor.execute(query)
            self.getConnection().commit()

            try:
                data = cursor.fetchall()
            except:
                pass
        finally:
            self.releaseCursor()

        return data

    def __del__(self):
        if (self.__db is not None):
            self.__db.close()

class DaoException(Exception):
    ''' Exception class for Dao objects. '''

    def __init__(self, message):
        Exception.__init__(self, message)