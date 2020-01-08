#import statements
import os
import time
import sys
from stat import *
from util.image_utils import *
from random import randint

def fileExists(filename):
    try:
        check = os.stat(filename).st_size > 0
        return check
    except OSError, (errno, strerror):
        if (errno == 2):
            # File not found error
            # Ignore this error because it's what we're looking for
            # print "OS error(%s): %s" % (errno, strerror)
            return False
        else:
            raise
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise

def dirExists(dirpath):
    try:
        check = S_ISDIR(os.stat(dirpath).st_mode)
        return check
    except OSError, (errno, strerror):
        if (errno == 2):
            # File not found error
            # Ignore this error because it's what we're looking for
            # print "OS error(%s): %s" % (errno, strerror)
            return False
        else:
            raise
    except:
        print "Unexpected error: ", sys.exc_info()[0]
        raise

def writeTextFile(filename, data, throwException = True):
    try:
        f = file(filename, 'w')
        f.write(data)
        f.flush()
        f.close()
    except IOError:
        if (throwException):
            raise 'Unable to write file: ' + filename
        else:
            pass


def log(data=None, filename='log.txt', showDate=True, throwException=False):
    try:
        f = file(filename, 'a+')
        if (data is None):
            data = ''
        if (showDate):
            data = (time.strftime('%A, %B %d, %Y %H:%M:%S', time.gmtime(time.time()))) + ': ' + str(data) + '\r\n'
        f.write(data)
        f.flush()
        f.close()
    except IOError:
        if (throwException):
            raise 'Unable to write file: ' + filename
        else:
            pass

def readTextFile(filename, throwException = True, replaceDict = None):
    data = None
    try:
        f = file(filename)
        data = f.read()
        f.close()

        if (replaceDict is not None):
            for item in replaceDict:
                data = data.replace('${' + item + '}', str(replaceDict[item]))
    except IOError:
        if (throwException):
            raise Exception('Unable to read file: ' + filename)
        else:
            pass

    return data


def getDirTreeSize(top):
    '''recursively descend the directory tree and count the file sizes'''

    data = 0

    for f in os.listdir(top):
        pathname = os.path.join(top, f)
        mode = os.stat(pathname)[ST_MODE]
        if S_ISDIR(mode):
            # It's a directory, recurse into it
            data += getDirTreeSize(pathname)
        elif S_ISREG(mode):
            # It's a file
            data += int(os.stat(pathname)[ST_SIZE])
        else:
            # Unknown file type, print a message
            pass

    return data

def getMultiDirTreeSize(dirlist):
    data = 0
    for item in dirlist:
        data += getDirTreeSize(item)
    return data


#class declarations
class FileCounter:

    counter = None
    basepath = ""
    path = ""
    semaphore = None

    def __init__(self, lclPath):
        self.basepath = str(lclPath)
        self.path = str(lclPath) + '/counter.txt'
        self.counter = 0

    def getCount(self):
        semaphore = Semaphore(str(self.basepath) + "counter")
        semaphore.wait()
        semaphore.put()

        check = False
        try:
            check = os.stat(self.path).st_size > 0
        except OSError, (errno, strerror):
            if (errno == 2):
                # File not found error
                # Ignore this error because it's what we're looking for
                check = False
            else:
                raise

        count = 1
        if (check):
           f = file(self.path, 'r')
           data = f.read()
           f.close()
           count = int(data)
           count = count + 1

        ff = file(self.path, 'w')
        ff.write(str(count))
        ff.flush()
        ff.close()

        semaphore.remove()
        self.counter = count
        return count

class Semaphore:

    waitLimit = 60

    def __init__(self, lclPath):
        self.path = lclPath + 'sem.txt'
        self.counter = 0

    def put(self):
        while (self.exists()):
            None

        try:
            f = file(self.path, 'w')
            f.write('DO NOT MANUALLY EDIT')
            f.flush()
            f.close()
        except:
            print "Unable to write semaphore"
            raise

    def remove(self):
        try:
            if (self.exists()):
                os.remove(self.path)
        except:
            print "Unable to remove semaphore"
            raise

    def exists(self):
        try:
            check = os.stat(self.path).st_size > 0
            if check:
                self.counter += 1
            else:
                self.counter = 0

            #Check count limit and remove old semaphore to
            #prevent lock-up
            if (self.counter > self.waitLimit):
                os.remove(self.path)
                self.counter = 0
                check = False

            return check
        except OSError, (errno, strerror):
            if (errno == 2):
                # File not found error
                # Ignore this error because it's what we're looking for
                # print "OS error(%s): %s" % (errno, strerror)
                return False
            else:
                raise
        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise

    def wait(self):
        #wait for the semaphore to be removed
        while(self.exists()):
            time.sleep(1)






