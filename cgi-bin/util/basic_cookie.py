# imports

import os
import Cookie
import cgi
from newscommunity.application import APPLICATION

#declarations

def verifyCookie(name = 'TODO: DEPRECATED', redirect=APPLICATION.redirectOnFailedLogin, userParser=None, form=None):
    nickname = None
    try:
        userkey = ''
        if ((form is not None) and form.has_key('userkey')):
            userkey = form.getfirst('userkey')
        else:
            cookie = os.environ["HTTP_COOKIE"]
            c2 = Cookie.SimpleCookie()
            c2.load(os.environ["HTTP_COOKIE"])
            userkey = c2[APPLICATION.cookieName].value
    except KeyError:
        print 'Location: ' + str(redirect) + '?e=ke'
        print
    else:
        nickname = userParser.unlock(userkey)

        if (nickname is None):
            print 'Location: ' + str(redirect) + '?e=ke2'
            print
            return None
    return nickname
