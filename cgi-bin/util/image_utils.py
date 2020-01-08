'''Package image_utils contains a class and utilities for basic
examination of image data.'''

import os

def isImageFile(filename):
    '''Test to see if the file is an acceptable filetype for an image file.'''
    check = False

    if (len(filename) > 4):
        ind = 4
        ext = filename[(len(filename) - ind):len(filename)]
        while (ext[0] != '.'):
            ext = filename[(len(filename) - ind):len(filename)]
            ind += 1

        extension = ext[1:len(ext)].upper()
        if ((extension == 'JPG') or (extension == 'JPEG') \
            or (extension == 'GIF') or(extension == 'PNG')):

            check = True
    return check

def getScaledWidth(height, width, newHeight):
    newWidth = int(float(width) / float(height) * float(newHeight))
    return newWidth

class ImageInfo:
    '''This class is used to examine an image to derive it's X and Y dimensions.
    The class can be used for most GIF, JPG, and PNG images.'''

    def __init__(self, filename):

        self.filename = filename
        self.height = -1
        self.width = -1
        self.extension = ''

        if (len(filename) > 4):
            ind = 4
            ext = filename[(len(filename) - ind):len(filename)]
            while (ext[0] != '.'):
                ext = filename[(len(filename) - ind):len(filename)]
                ind += 1

            self.extension = ext[1:len(ext)].upper()

            if ((self.extension == 'JPG') or (self.extension == 'JPEG')):
                self.__inspectJpg__(filename)
            elif (self.extension == 'GIF'):
                self.__inspectGif__(filename)
            elif (self.extension == 'PNG'):
                self.__inspectPng__(filename)
            else:
                raise 'Invalid image filename:', filename

    def __inspectJpg__(self, filename):
        '''This method does not currently watch for thumbnails.'''

        # getting x and y dimensions from a jpeg/jpg in python
        # bigendian
        try:
            f = file(filename, 'rb') #read-only, binary
            b = None
            while(1):
                c = f.read(1)
                if (b is not None):
                    #ffc0 is the header key for image information
                    if ((hex(ord(b)) == '0xff') and (hex(ord(c)) == '0xc0')):
                        break
                b = c

            junk = f.read(3)
            y = f.read(2)
            x = f.read(2)
            f.close()

            self.height = self.intFromBytes(y)
            self.width = self.intFromBytes(x)

        except IOError:
            raise "IOError attempting to access:", filename

    def __inspectGif__(self, filename):
        '''Should work for basic Gif's.'''

        # getting x and y dimensions from a gif in python
        # littleendian
        try:
            f = file(filename, 'rb')
            junk = f.read(6)
            x = f.read(2)
            y = f.read(2)
            f.close()

            self.height = self.intFromBytes(y, 0)
            self.width = self.intFromBytes(x, 0)

        except IOError:
            raise "IOError attempting to access:", filename

    def __inspectPng__(self, filename):
        '''Should work for basic Gif's.'''

        # getting x and y dimensions from a PNG in python
        # bigendian
        try:
            f = file(filename, 'rb')
            junk = f.read(16)
            x = f.read(4)
            y = f.read(4)
            f.close()

            self.height = self.intFromBytes(y)
            self.width = self.intFromBytes(x)

        except IOError:
            raise "IOError attempting to access:", filename

#    def intFromBytes(self, bytes, bigEndian = True): # Doesn't work in Pyton 2.0
    def intFromBytes(self, bytes, bigEndian = 1):
        '''Convert a string of bytes to an int after first generating a hex value.'''
        myhex = ''
        for i in range(0, len(bytes)):
            if (bigEndian == 1):
                j = i
            else:
                j = len(bytes) - i - 1
            thex = hex(ord(bytes[j]))
            digits = thex[2:len(thex)]
            if (len(digits) == 2):
                myhex += digits
            else:
                myhex = myhex + '0' + digits
        myhex = '0x' + myhex

        return int(myhex, 16)

    def toString(self):
        print "Image: ", self.filename
        print "\tExtension: ", self.extension
        print "\tWidth: ", self.width
        print "\tHeight: ", self.height

