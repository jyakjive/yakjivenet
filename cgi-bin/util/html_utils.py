# imports
from newscommunity.ncvars import *
from util.utils import remember
#from datetime import *
import time
from random import *
from text_utils import *

remember('counter', 0)

def getTodayDateString():
#    #June 14, 2005
#    data = datetime.today().strftime('%A, %B %d, %Y')
    data = time.strftime('%A, %B %d, %Y', time.gmtime(time.time()))
    return str(data)

def getTodayHTML():
    data = '<span class="todaysDate">' + getTodayDateString() + '</span>'
    return str(data)

def miloSayingGenerator():
    miloSayings = [ \
        'Milo is watching', \
        'Milo says don\'t forget to save', \
        'Milo likes you', \
        'Milo is your friend', \
        'Milo will take you home', \
        'Milo is smarter than...', \
        'Milo wants a treat!', \
        'Milo says, "Don\'t forget to feed me!"', \
        'Milo says Jezebel is a fat cat', \
        'Milo is sleepy', \
        'Poor Milo just wants play time', \
        'Milo reminds you to contribute to the Humane Society']

    data = ''

    seed()
    data = miloSayings[randint(0, len(miloSayings) - 1)]

    return data

# definitions
def printPage(headerFile, body, footerFile, replaceDict = None, cookie = None):
    ''' Load the header and footer and print the body, header and footer to the standard output.
        DONE: Added the ability to replace keys in the header and footer using replaceDict.
    '''
    #Load the header file
    f = file(headerFile)
    header = f.read()
    f.close

    #Load the footer file
    f = file(footerFile)
    footer = f.read()
    f.close

    if (replaceDict is not None):
        for item in replaceDict:
            header = header.replace('${' + item + '}', replaceDict[item])
            footer = footer.replace('${' + item + '}', replaceDict[item])

    print "Content-Type: text/html"     # HTML is following
    if (cookie is not None):
        print cookie
    print                               # blank line, end of headers

    print header
    print body
    print footer

def printPage2(theFile=None, body='', replaceDict = None, cookie = None):
    ''' Load a template file and print file to the standard output.
        DONE: Add the ability to replace keys in the header and footer using replaceDict.
    '''
    #Load the header file
    page = '${body}'
    if ((theFile is not None) and (theFile != '')):
        f = file(theFile)
        page = f.read()
        f.close

    if (replaceDict is not None):
        for item in replaceDict:
            page = page.replace('${' + item + '}', replaceDict[item])

    page = page.replace('${body}', body)

    print "Content-Type: text/html"     # HTML is following
    if (cookie is not None):
        print cookie
    print                               # blank line, end of headers

    print page

def createTextInput(name, value = '', size = 20, maxLength = None, disabled = 'False',
        onclick = None, onchange = None, onkeyup = None, onblur = None):
    ''' Print a simple TEXT INPUT type. '''
    if (value is None):
        value = ''
    data = '<INPUT TYPE="TEXT" NAME="' + toSafeHTML(name) + \
        '" VALUE="' + toSafeHTML(value) + \
        '" SIZE="' + str(size) + '"'
    if (maxLength is not None):
        data += ' MAXLENGTH="' +  str(maxLength) + '"'
    if (disabled in TRUE):
        data += ' DISABLED'
    if (onclick is not None):
        data += ' ONCLICK="' + onclick + '"'
    if (onchange is not None):
        data += ' ONCHANGE="' + onchange + '"'
    if (onkeyup is not None):
        data += ' onKeyUp="' + onkeyup + '"'
    if (onblur is not None):
        data += ' onBlur="' + onblur + '"'
    data += '>\n'
    return data

def createTextArea(name, value = '', rows = 5, cols = 30, maxchars = 500, formName = None,
        onclick = None):
    if (maxchars is None):
        raise 'maxchars must be non-None in textarea'
    if (value is None):
        value = ''
    tcname = 'tc_' + name
    data = '<textarea name="' + str(name) + \
        '" rows="' + str(rows) + '" cols="' + str(cols) + '"'
    countJScript = ''
    if (formName is None):
        countJScript = 'javascript:textCounter(getIt(\'' + name + \
            '\'), getIt(\'' + tcname + '\'), ' + str(maxchars) + ')'
    else:
        countJScript = 'javascript:textCounter(getFromForm(\'' + name + \
            '\', \'' + formName + '\'), getFromForm(\'' + tcname + '\', \'' + formName + '\'), ' + str(maxchars) + ')'
    data += ' onKeyDown="' + countJScript + '"'
    data += ' onKeyUp="' + countJScript + '"'
    if (onclick is not None):
        data += ' ONCLICK="' + onclick + '"'
    data += '>'
    data += toSafeHTML(value)
    data += '</textarea><br>\n'
    data += createTextInput(tcname, (maxchars - len(value)), 5, None, True) + ' characters left\n'
    return data

def createPasswordInput(name, value = '', size = 20, maxLength = None, disabled = 'False',
        onclick = None):
    ''' Print a simple PASSWORD INPUT type. '''
    if (value is None):
        value = ''
    data = '<INPUT TYPE="PASSWORD" NAME="' + str(name) + \
        '" VALUE="' + toSafeHTML(value) + \
        '" SIZE="' + str(size) + '"'
    if (maxLength is not None):
        data += ' MAXLENGTH="' +  str(maxLength) + '"'
    if (disabled in TRUE):
        data += ' DISABLED'
    if (onclick is not None):
        data += ' ONCLICK="' + onclick + '"'
    data += '>\n'
    return data

def createCheckBox(name, value = '', checked = 'False', disabled = 'False', clazz = None,
        onclick = None):
    ''' Print a simple CHECKBOX INPUT type. '''
    data = '<INPUT TYPE="CHECKBOX" NAME="' + str(name) + \
        '" VALUE="' + toSafeHTML(value) + '"'
    if (checked in TRUE):
        data += ' CHECKED'
    if (disabled in TRUE):
        data += ' DISABLED'
    if (clazz is not None):
        data += ' CLASS="' + clazz + '"'
    if (onclick is not None):
        data += ' ONCLICK="' + onclick + '"'
    data += '>\n'
    return data

def createRadioItem(name, value = '', checked = 'False', disabled = 'False', clazz = None,
        onclick = None):
    ''' Print a simple RADIO INPUT type. '''
    data = '<INPUT TYPE="RADIO" NAME="' + str(name) + \
        '" VALUE="' + toSafeHTML(value) + '"'
    if (checked in TRUE):
        data += ' CHECKED'
    if (checked in TRUE):
        data += ' DISABLED'
    if (clazz is not None):
        data += ' CLASS="' + clazz + '"'
    if (onclick is not None):
        data += ' ONCLICK="' + onclick + '"'
    data += '>\n'
    return data

def createHiddenInput(name, value = ''):
    ''' Print a simple HIDDEN INPUT type. '''
    data = '<INPUT TYPE="HIDDEN" NAME="' + str(name) + \
        '" VALUE="' + toSafeHTML(value) + '">\n'
    return data

def createSelect(name, options, defaultOption = '', size = 1, multiple = 'False', \
        sorted = 'True', disabled = 'False', onclick = None, onchange=None):
    ''' Print a select given a dictionary of options (value:screen display value). '''
    data = '<SELECT NAME="' +  str(name) + '"'
    data += ' SIZE="' + str(size) + '"'
    if (multiple in TRUE):
        data += ' MULTIPLE'
    if (disabled in TRUE):
        data += ' DISABLED'
    if (onclick is not None):
        data += ' ONCLICK="' + onclick + '"'
    if (onchange is not None):
        data += ' ONCHANGE="' + onchange + '"'
    data += '>\n'
    if (options is not None):
        if (type(options) == type(list())):
            if (sorted == 'True'):
                options.sort()
            for item in options:
                data += '\t<OPTION VALUE="' +  toSafeHTML(item) + '"'
                if (defaultOption == item):
                    data += ' SELECTED'
                data += '>' +  str(item) + '\n'
        elif (type(options) == type(dict())):
            okeys = options.keys()
            if (sorted == 'True'):
                okeys.sort()
            for item in okeys:
                data += '\t<OPTION VALUE="' +  toSafeHTML(item) + '"'
                if (defaultOption == item):
                    data += ' SELECTED'
                data += '>' +  str(options[item]) + '\n'
    data += '</SELECT>\n'
    return data

def createSelect2(name, options, values, defaultOption = '', size = 1, multiple = 'False', \
        disabled = 'False', onclick = None):
    ''' Print a select given lists of options and values. Not sorted! '''
    data = '<SELECT NAME="' +  str(name) + '"'
    data += ' SIZE="' + str(size) + '"'
    if (multiple in TRUE):
        data += ' MULTIPLE'
    if (disabled in TRUE):
        data += ' DISABLED'
    if (onclick is not None):
        data += ' ONCLICK="' + onclick + '"'
    data += '>\n'
    if (options is not None):
        for i in range(len(options)):
            data += '\t<OPTION VALUE="' +  toSafeHTML(values[i]) + '"'
            if (defaultOption == values[i]):
                data += ' SELECTED'
            data += '>' +  str(options[i]) + '\n'
    data += '</SELECT>\n'
    return data

def createButton(name, text, value = '', onclick = None, type = 'BUTTON', disabled = 'False'):
    ''' Print a simple TEXT INPUT type. '''
    data = '<BUTTON TYPE="BUTTON" NAME="' + str(name) + \
        '" VALUE="' + str(value) + '"'
    if (onclick is not None):
        data += ' ONCLICK="' +  str(onclick) + '"'
    if ((disabled == '1') or (disabled == 'True')):
        data += ' DISABLED'
    data += '>' + text + '</BUTTON>\n'
    return data

def createLink(href, title = None, text = None, img = None, clazz = '',
        id = None, target = None, noFollow=False, inPage=False,
        onmouseover=None, onmouseout=None):
    '''Print a simple anchor.'''
    data = ''
    if (inPage):
        data += '<A NAME="' + str(href) + '"'
    else:
        data += '<A HREF="' + str(href) + '"'
    if ((title is not None) and (title != '')):
        data += ' TITLE="' + toSafeHTML(title) + '"'
    if ((id is not None) and (id != '')):
        data += ' ID="' + toSafeHTML(id) + '"'
    if (clazz != ''):
        data += ' CLASS="' + toSafeHTML(clazz) + '"'
    if ((target is not None) and (target != '')):
        data += ' TARGET="' + toSafeHTML(target) + '"'
    if (noFollow):
        data += ' rel="nofollow"'
    if (onmouseover is not None):
        data += ' ONMOUSEOVER="' + toSafeHTML(onmouseover) + '"'
    if (onmouseout is not None):
        data += ' ONMOUSEOUT="' + toSafeHTML(onmouseout) + '"'
    data += '>'
    if (text is not None):
        data += str(text)
    elif (img is not None):
        data += '<IMG SRC="' + str(img) + '">'
    else:
        raise 'html_utils.createLink requires text or an image url.'
    data += '</A>'
    return data

def createHelpLink(title, text, helpInfo, img = None, inline = 'True', clazz = 'helplinktext', \
    xshift = 0, yshift = -20):
    '''Print a simple div and anchor to display help information.'''
    counter = remember('counter')
    helplink = 'helplink' + str(counter)
    helpdiv = 'helpdiv' + str(counter)
    if (inline in TRUE):
        helpJScript = 'javascript:toggleDiv(\'' + helpdiv + '\');'
        helpInfo += '\n<br>&nbsp;<br><a href="javascript:toggleDiv(\'' + helpdiv + '\');"' + \
            ' title="Hide help window">[close]</a>'
        data = createLink(helpJScript, title, text, img, clazz, helplink);
        data += '<DIV ID="helpdiv' + str(counter) + \
            '" CLASS="helpdiv" STYLE="display: none;">\n' + \
            helpInfo + '\n</DIV>\n'
    else:
        helpJScript = 'javascript:showHelpWin(\'' + helplink + '\',\'' + \
            helpdiv + '\', ' + str(xshift) + ', ' + str(yshift) + ');'
        helpInfo += '\n<br>&nbsp;<br><a href="javascript:toggleDiv(\'' + helpdiv + '\');"' + \
            ' title="Hide help window">[close]</a>'
        data = createLink(helpJScript, title, text, img, clazz, helplink);
        data += '<DIV ID="helpdiv' + str(counter) + \
            '" CLASS="helpdiv2" STYLE="position:absolute;z-index:10;display: none;width:250;">\n' + \
            helpInfo + '\n</DIV>\n'
    remember('counter', counter + 1)
    return data

def createPopupLink(title, text, body, img = None, inline = 'True', clazz = 'helplinktext', \
    xshift = 0, yshift = -20, divID = None, divClazz = None):
    '''Print a simple div and anchor to display popup information.'''
    counter = remember('counter')
    helplink = 'helplink' + str(counter)
    if (divID is None):
        helpdiv = 'pdiv' + str(counter)
    else:
        helpdiv = divID
    if (divClazz is None):
        divClazz = clazz
    if (inline in TRUE):
        helpJScript = 'javascript:toggleDiv(\'' + helpdiv + '\');'
        body += '\n<br><a href="javascript:toggleDiv(\'' + helpdiv + '\');"' + \
            ' title="Hide help window">[close]</a>'
        data = createLink(helpJScript, title, text, img, clazz, helplink);
        data += '<DIV ID="' + helpdiv + \
            '" CLASS="' + divClazz + '" STYLE="display: none;">\n' + \
            body + '\n</DIV>\n'
    else:
        helpJScript = 'javascript:showHelpWin(\'' + helplink + '\',\'' + \
            helpdiv + '\', ' + str(xshift) + ', ' + str(yshift) + ');'
        body += '\n<br><a href="javascript:toggleDiv(\'' + helpdiv + '\');"' + \
            ' title="Hide window">[close]</a>'
        data = createLink(helpJScript, title, text, img, clazz, helplink);
        data += '<DIV ID="' + helpdiv + \
            '" CLASS="' + divClazz + '" STYLE="position:absolute;z-index:10;display: none;width:250;">\n' + \
            body + '\n</DIV>\n'
    remember('counter', counter + 1)
    return data

def createFloatingDiv(title, text, body, divId, inline = 'True', clazz = '', \
    xshift = 0, yshift = -20, img = None):
    '''Print a simple div and anchor to display help information.'''
    dlink = divId + '_link'
    if (inline in TRUE):
        dJScript = 'javascript:toggleDiv(\'' + divId + '\');'
        body += '\n<br><a href="javascript:toggleDiv(\'' + divId + '\');"' + \
            ' title="Hide help window">[close]</a>'
        data = createLink(dJScript, title, text, img, clazz, dlink);
        data += '<DIV ID="' + divId + \
            '" CLASS="helpdiv" STYLE="display: none;">\n' + \
            body + '\n</DIV>\n'
    else:
        dJScript = 'javascript:showHelpWin(\'' + dlink + '\',\'' + \
            divId + '\', ' + str(xshift) + ', ' + str(yshift) + ');'
        body += '\n<br>\n<a href="javascript:toggleDiv(\'' + divId + '\');"' + \
            ' title="Hide window">[close]</a>'
        data = createLink(dJScript, title, text, img, clazz, dlink) + '\n'
        data += '<DIV ID="' + divId + \
            '" CLASS="helpdiv2" STYLE="position:absolute;z-index:10;display: none;width:250;">\n' + \
            body + '\n</DIV>\n'
    return data

def createForm(name, action, method, body, encoding = None, target = None, onSubmit=None):
    ''' Create a form.  Note that you have to pass in the body already formatted. '''
    data = '<FORM ACTION="' + action + '" NAME="' + name + '"'
    data += ' METHOD="' + method + '"'
    if (encoding is not None):
        data += ' ENCTYPE="' + encoding + '"'
    if (target is not None):
        data += ' TARGET="' + target + '"'
    if (onSubmit is not None):
        data += ' onSubmit="' + onSubmit + '"'
    data += '>\n'
    data += body
    data += '</FORM>\n'
    return data

def checkNbsp(value):
    data = value
    if ((value is None) or (value == '')):
        data = '&nbsp;'
    return data
