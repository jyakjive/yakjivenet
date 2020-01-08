import os

# Definitions

def checkReferer(checkString, firstPosition = False):
    ''' Looks to see if a particular string is in the HTTP_REFERER env variable.
        Note: If the HTTP_REFERER is not in the env, it will look for
        REMOTE_ADDR and SERVER_ADDR.  If these are not found, it will throw an
        exception.  The biggest problem on this is what happens in the event
        of clustering?
    '''
    check = False
    key1 = 'HTTP_REFERER'
    key2 = 'REMOTE_ADDR'
    key3 = 'SERVER_ADDR'

    # Check the first n positions in the remote and server IP's
    checkPositions = 3

    if (key1 in os.environ):
        if (firstPosition):
            check = (os.environ[key1].find(checkString) == 0)
        else:
            check = checkString in os.environ[key1]
    else:
        if ((key2 in os.environ) and (key3 in os.environ)):
            val2 = os.environ[key2]
            val3 = os.environ[key3]

            val2 = val2.split('.')
            val3 = val3.split('.')

            for i in range(0,checkPositions):
                check = check and (val2[i] == val3[i])

        else:
            raise Exception('Unable to check referer')

    return check