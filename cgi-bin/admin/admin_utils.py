
# imports
from random import randint
from vars import *

# defs

def getRandomKey(multipleOfThree):
    randchars = ''
    for i in range(multipleOfThree):
        randchars += chr(randint(65,90))
        randchars += chr(randint(97,122))
        randchars += chr(randint(48,57))
    return randchars

def checkAlphaNum(value, additionalChars = None):
    check = True

    anChars = ALPHANUM_CHARS
    if (additionalChars is not None):
        anChars += additionalChars

    if (value is not None):
        for i in value:
            check = check and (i in anChars)
            if (not check):
                break
    else:
        check = False

    return check