#import statements
import os
import time
import sys
from stat import *
from newscommunity.ncvars import *
from newscommunity.application import APPLICATION
from util.image_utils import *
from random import randint
from fileutils import *
from math import *
from db.attachment_dao import Attachment

IM_LOCATION = '/usr/bin/convert'

def resizeIM(inFile, width, outFile):
    ''' Resize an image using ImageMagick.'''
    retVal = os.spawnl(os.P_WAIT, IM_LOCATION, IM_LOCATION, inFile, '-resize', str(width), outFile)
    return retVal

# NOTE: This is a very NC specific method
def uploadFile(fileitem, attachment, attachDirectory, \
        limitSize = True, photoOnly = False):
    ''' Upload a file.  Image files will be automatically
        resized if the flag is set to do so in the APPLICATION properties.
        Also generated a thumbnail.
    '''
    check = True
    test = ''
    sem = Semaphore(attachDirectory + 'attach_')
    esem = Semaphore(attachDirectory + 'error_')
    msg = ''
    try:
        if (fileitem is not None):
            if fileitem.file:
                temp = fileitem.filename
                temp = temp.replace('\\', '/')
                temp = temp.split('/')
                temp = temp[len(temp) - 1]
                test = temp
                attachment.originalFilename = str(temp)
                attachment.filename = str(randint(0,1000000000)) + 'r_' + str(temp)

                sem.put()
                newFile = file(attachDirectory + attachment.filename, 'wb')

                while 1:
                    data = fileitem.file.read(1)
                    if not data: break
                    newFile.write(data)

                newFile.flush()
                newFile.close()

                attachment.size = os.stat(attachDirectory + attachment.filename).st_size
                if (limitSize):
                    check = (attachment.size < FILE_SIZE_BASIC)
                else:
                    check = (attachment.size < FILE_SIZE_MAX)

                # Create the absolute path to the files
                # TODO: Genericize this
                absPath = APPLICATION.absoluteRootPath
                tPath = attachDirectory
                while ('../' in tPath):
                    tPath = tPath.replace('../', '')
                absPath += tPath

                # If image resizing is allowed, resize the image to fit under the allowed size
                if (APPLICATION.autoResizeImages):

                    # calculate the amount to shrink the image

                    sidePct = 1
                    if (limitSize):
                        sidePct = int(100 * sqrt(1.0 * FILE_SIZE_BASIC / attachment.size))
                    else:
                        sidePct = int(100 * sqrt(1.0 * FILE_SIZE_MAX / attachment.size))

                    inFile = absPath + attachment.filename
                    outFile = absPath + 'r_' + attachment.filename
                    spawnReturn = resizeIM(inFile, str(sidePct) + '%', outFile)

                    if (spawnReturn == 0):
                        # return the old file and use the shrunken file
                        os.remove(attachDirectory + attachment.filename)
                        attachment.filename = 'r_' + attachment.filename
                        attachment.size = os.stat(attachDirectory + attachment.filename).st_size
                        check = True
                    else:
                        msg += 'RESIZE: Unable to create ' + outFile + ' : ' + str(spawnReturn) + '\r\n'

                if (not check):
                    os.remove(attachDirectory + attachment.filename)
                    msg += attachment.filename + ' deleted because file was too big.\r\n'
                else:
                    if (isImageFile(attachment.filename)):
                        info = ImageInfo(attachDirectory + attachment.filename)
                        attachment.imageHeight = info.height
                        attachment.imageWidth = info.width
                        attachment.image = True
                        attachment.thumbnailName = 't_' + attachment.filename

                        # raise Exception(absPath)

                        inFile = absPath + attachment.filename
                        outFile = absPath + attachment.thumbnailName

                        attachment.thumbnailHeight = int(APPLICATION.imageSize)
                        attachment.thumbnailWidth = int(getScaledWidth(attachment.imageHeight, attachment.imageWidth, attachment.thumbnailHeight))

                        spawnReturn = resizeIM(inFile, attachment.thumbnailWidth, outFile)

                        #outFile = outFile[0:len(outFile)-3] + 'png'
                        #spawnReturn = os.spawnl(os.P_WAIT, '/usr/bin/convert', '/usr/bin/convert', inFile, '-resize', '50%', outFile)

                        if (spawnReturn > 0):
                            msg += 'THUMB: Unable to create ' + outFile + ' : ' + str(spawnReturn) + '\r\n'
                    else:
                        # TODO - use FILE_TYPES_ALLOWED to limit the types of files accepted
                        if (photoOnly):
                            check = isImageFile(attachment.filename)
                            if (not check):
                                os.remove(attachDirectory + attachment.filename)
                                msg = attachment.filename + \
                                    ' deleted because file must be of type image.'

            else:
                check = False
            sem.remove()
    except IOError:
        check = False
        # TODO-L: Write a mechanism to clean up or scan this log
        msg += 'NO-SAVE:' + fileitem.filename + test + '\n'
        sem.remove()

    if (msg != ''):
        esem.put()
        errorLog = file(attachDirectory + 'error.log', 'a+')
        errorLog.write(msg)
        errorLog.flush()
        errorLog.close()
        esem.remove()
    return check






