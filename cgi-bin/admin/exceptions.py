
#imports
import sys
import traceback
from utils import remember
from classes.admin_console_html import *
from newscommunity.application import APPLICATION
from fileutils import readTextFile
from email import sendEmail
from vars import *

#define the new excepthook
def ecardhook(etype, message, obj):

    msg = ''
    #Exception when a card file cannot be found
    if (str(etype) == "exceptions.IOError"):
        msg = "The item you requested could not be found.(1: IOError)"

    #Exception when a greeting card category cannot be found
    if (str(etype) == "exceptions.TypeError"):
        msg = "The item you requested could not be found.(2: TypeError)"

    #Exception on the edit page when a card category is not found
    if (message == None):
        msg= "The item you requested could not be found.(3)"

    #Exception when someone enters bad data in a url
    if (str(etype) == "exceptions.ValueError"):
        msg = "An unexpected error has occurred."

    # traceback.print_exception(etype, message, obj)

    body = '''
<table width="600" border="0">
<tr><td width="10%">&nbsp;
<th align="LEFT">
<h1>Error</h1>
&nbsp;
<p>We apologize, but you have encountered an unexpected error<br>
&nbsp;
<p>The error has been logged with YakJive.com and we will investigate<br>
as soon as possible.  Please <a href="''' + APPLICATION.startPage + '''">click here</a> to return to<br>
your start page.<br>
&nbsp;
<p>If you continue to encounter the error, please<br>
<a href="http://www.yakjive.com/yjcontact.html">contact us immediately</a> to indicate<br>
that your site is experiencing technical difficulties.<br>
&nbsp;
<p>We are sorry for any incovenience.  Thank you for using YakJive.com.
</table>
'''

    emailBody = msg + '<br>&nbsp;<br>\n'

    data = traceback.format_tb(obj)

    for item in data:
        emailBody += str(item).replace('\n', '<br>') + '<br>\n'
    emailBody += str(etype) + '<br>\n'
    emailBody += str(message) + '<br>\n'

    emailDict = dict()
    emailDict['error'] = emailBody
    emailDict['domain'] = APPLICATION.domainName
    # TODO: Soft-code the email addresses somewhere
    emailDict['fromEmail'] = 'problem@yakjive.com'
    emailDict['toEmail'] = 'problem@yakjive.com'
    emailDict['subject'] = 'YakJive Exception -- ' + APPLICATION.domainName + ': ' + str(etype)
    emailBody = readTextFile(FILENAME_EMAIL_ERROR, False, emailDict)

    if (GLOBAL_DEBUG):
        body += emailBody

    try:
        sendEmail(emailDict['fromEmail'], emailDict['toEmail'], email)
    except:
        # don't keep throwing exceptions
        # TODO: Log this condition
        pass

    replaceDict = {'userWelcome':''}
    printConsolePage(body, replaceDict)

def handleExceptions():
    sys.excepthook = ecardhook

