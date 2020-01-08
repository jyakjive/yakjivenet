#!/usr/bin/python
##!D:/Python27/python.exe

from util.html_utils import *
from ui.os_extras import *
from admin.vars import *
from util.fileutils import *
import cgi
import util.exceptions
from admin.mvc_admin import *

util.exceptions.handleExceptions()

# TODO: filter the potential people who can come in here

title = ''
itemTitle = ''


categoryList = [
    'Newsletter',
    'Newspaper',
    'Hobby',
    'Personal',
    'Non-profit organization',
    'Club',
    'Family',
    'Business']

form = cgi.FieldStorage()

check = False
if (form.has_key('referer') and (form.getfirst('referer') == INTERNAL_REFERER)):
    check = True
inviteCode = form.getfirst('inviteCode')
check = check and (inviteCode is not None)

errorMessage = ''
if (form.has_key('errorMessage')):
    errorMessage = form.getfirst('errorMessage')

domain = form.getfirst('domain')
siteCategory = form.getfirst('siteCategory')
siteTitle = form.getfirst('siteTitle')
siteSubTitle = form.getfirst('siteSubTitle')
companyName = form.getfirst('companyName')
metaKeywords = form.getfirst('metaKeywords')
metaDescription = form.getfirst('metaDescription')
webmasterEmail = form.getfirst('webmasterEmail')
webmasterFirst = form.getfirst('webmasterFirst')
webmasterLast = form.getfirst('webmasterLast')
webmasterUsername = form.getfirst('webmasterUsername')
webmasterPassword = form.getfirst('webmasterPassword1')
webmasterNickname = form.getfirst('webmasterNickname')

if (check):

    body = '''
<script>
function checkLocalValue(name, formName, message, alphaNum){

    var checkAN = (alphaNum == true);

    var obj = getFromForm(name, formName);
    var vCheck = (obj.value != '');
    if (checkAN){
        vCheck = vCheck && isAlphaNum(obj.value);
    }
    if (!vCheck){
        if (checkAN){
            message += '\\nThe value must contain no spaces or special characters\\nother than hyphens (-) or underscores (_).';
        }
        alert(message);
        obj.focus();
    }
    return vCheck;
}

function checkPasswordValues(pwd1, pwd2, formName, minLength, message){
    var val1 = getFromForm(pwd1, formName).value;
    var val2 = getFromForm(pwd2, formName).value;
    
    var vCheck = true;
    vCheck = vCheck && (val1 == val2) && (val1.length >= minLength);
    
    if (!vCheck){
        alert(message);
        getFromForm(pwd1, formName).focus();
    }
    return vCheck;
}

function doSubmit(){
    var check = true;

    check = check && checkLocalValue('domain', 'siteForm',
        'You must fill in a value for the domain.\\nThe domain is the name of your site.', true);
    check = check?(check && checkLocalValue('webmasterNickname', 'siteForm',
        'You must choose a penname.\\nThe penname is your \\'autograph\\' on the site.', false)): check;
    check = check?(check && checkLocalValue('webmasterUsername', 'siteForm',
        'You must choose a username for your login.\\nYour username and penname should be different.', true)): check;
    if (check && (getFromForm('webmasterNickname', 'siteForm').value == getFromForm('webmasterUsername', 'siteForm').value)){
        check = false;
        alert('For the security of your site, your penname and username must be different.');
        getFromForm('webmasterNickname', 'siteForm').focus();
    }

// bug fix 1-3-2020
    check = check?(check && checkPasswordValues('webmasterPassword1', 'webmasterPassword2', 'siteForm', 6, 
        'Please fill in both password fields with the same value.\\nPasswords should be at least 6 characters.')):check;
        
//    check = check?(check && checkLocalValue('webmasterPassword1', 'siteForm',
//        'Please fill in both password fields with the same value.\\nPasswords should be at least 6 characters.') &&
//        (getFromForm('webmasterPassword1', 'siteForm').value.length > 5)): check;
//    check = check?(check && checkLocalValue('webmasterPassword2', 'siteForm',
//        'Please fill in both password fields with the same value.\\nPasswords should be at least 6 characters.') &&
//        (getFromForm('webmasterPassword2', 'siteForm').value.length > 5)): check;
    check = check?(check && checkLocalValue('webmasterFirst', 'siteForm',
        'You must enter a first name.')): check;
    check = check?(check && checkLocalValue('webmasterEmail', 'siteForm',
        'You must enter an email address.', false)): check;
    if (check){
        if (!checkValidEmail(getFromForm('webmasterEmail', 'siteForm').value)){
            alert('You must enter a valid email address.');
            return check;
        }
        check = check?(check && checkLocalValue('siteTitle', 'siteForm',
            'You must enter a title for your site.')): check;

        if (!check){
            return check;
        }

        //var sel = getFromForm('siteCategory', 'siteForm');
        //check = check && (sel.selectedIndex > -1);
        //if (!check){
        //    alert('You must select a site category.');
        //    sel.focus();
        //}
    }
    if (check){
        check = check && getFromForm('terms', 'siteForm').checked;
        if (!check){
            alert('You must accept the terms and conditions to continue.');
            getFromForm('terms', 'siteForm').focus();
        }
    }
    if (check){
        getForm('siteForm').submit();
    }
}
</script>
'''

    fbody = '<table border="0" width="600" class="siteInfoTable">\n'
    fbody += '<TR><th colspan="2">Fill in this form to create your website!  ' + \
        'Items marked with an asterisk (*) are required. Please note that your site name, ' + \
        'penname, and username cannot be changed after completing the registration process.\n'
    fbody += '<TR><th colspan="2">&nbsp;\n'
    if (errorMessage != ''):
        fbody += '<TR><th colspan="2"><span class="warning">' + errorMessage + '</span>\n'
        fbody += '<TR><th colspan="2">&nbsp;\n'
    fbody += '<TR><th scope="row" align="left" width="30%">Your site name*:<td align="left">http://www.yakjive.com/' + createTextInput('domain', domain) + '\n'
    fbody += '<TR><th colspan="2">&nbsp;\n'
    #fbody += '<TR><th colspan="2">Webmaster\'s information\n'
    fbody += '<TR><th scope="row" align="left">Penname*:<td align="left">' + createTextInput('webmasterNickname', webmasterNickname) + '\n'
    fbody += '<TR><th scope="row" align="left">Username*:<td align="left">' + createTextInput('webmasterUsername', webmasterUsername) + '\n'
    fbody += '<TR><th scope="row" align="left">Password*:<td align="left">' + createPasswordInput('webmasterPassword1', webmasterPassword) + '\n'
    fbody += '<TR><th scope="row" align="left">Password*: (again)<td align="left">' + createPasswordInput('webmasterPassword2', webmasterPassword) + '\n'
    fbody += '<TR><th scope="row" align="left">First name*<td align="left">' + createTextInput('webmasterFirst', webmasterFirst) + '\n'
    fbody += '<TR><th scope="row" align="left">Last name<td align="left">' + createTextInput('webmasterLast', webmasterLast) + '\n'
    #fbody += '<TR><th scope="row" align="left">Company name<td align="left">' + createTextInput('companyName', companyName) + '\n'
    fbody += '<TR><th scope="row" align="left">Email*<td align="left">' + createTextInput('webmasterEmail', webmasterEmail) + '\n'
    #fbody += '<TR><th colspan="2">&nbsp;\n'
    #fbody += '<TR><th colspan="2">Site information\n'
    fbody += '<TR><th scope="row" align="left">Descriptive site title*:<td align="left">' + createTextInput('siteTitle', siteTitle) + '\n'
    #fbody += '<TR><th>Site subtitle:<td align="left">' + createTextInput('siteSubTitle', siteSubTitle) + '\n'
    #fbody += '<TR><th>Site category*:<td align="left">' + createSelect('siteCategory', categoryList, siteCategory) + '\n'
    #fbody += '<TR><th>Site keywords:<td align="left">' + createTextInput('metaKeywords', metaKeywords, 40, 100) + '\n'
    #fbody += '<TR><th>Site Description<td align="left">' + createTextInput('metaDescription', metaDescription, 40, 255) + '\n'
    fbody += '<tr><td colspan="2">&nbsp;\n'
    fbody += '<tr><th colspan="2">' + \
            createLink('http://www.yakjive.com/messages/terms-and-conditions.html',
            'Review the terms and conditions',
            'Please review the terms and conditions',
            target="terms and conditions")
    fbody += '<tr><td colspan="2">&nbsp;\n'
    fbody += '<tr><th width="10%" colspan="2">I agree with the YakJive.com<br>Terms and Conditions of Service:<br>\n'
    fbody += createCheckBox('terms', 'True', clazz='plaininput') + '\n'

    fbody += '<noscript><br>For text browser users:\n + ' + createSubmit('SUBMIT', 'Create my site', 'Click to create your site') + '</noscript>\n'
    fbody += '<TR><TD COLSPAN="2">' + createButton('SUBMIT', 'SUBMIT', 'SUBMIT', onclick='javascript:doSubmit();', type = 'SUBMIT') + '\n'
    fbody += '<TR><th colspan="2">&nbsp;\n'

    fbody += createHiddenInput('inviteCode', inviteCode)
    fbody += createHiddenInput('operation', OP_CREATE_SITE)
    fbody += '</TABLE>'

#    fix on 1-3-2019
#    body += '<HTML><HEAD><TITLE>Add site</TITLE></HEAD><BODY>' + createForm('siteForm', 'dispatch_site_creation.py', 'POST', fbody) + '</BODY>'
    body += createForm('siteForm', 'dispatch_site_creation.py', 'POST', fbody)

else:

    body = '''
<p>We apologize, but we are not able to process your request at this time.
<p>If you would like to request a valid invite code, please <a href="http://www.yakjive.com/yjcontact.html">send us a message.</a>
'''

    if (inviteCode is None):
        body += ' 1'

replaceDict = dict()
if (errorMessage == ''):
    replaceDict['title'] = 'Enter site information'
else:
    replaceDict['title'] = 'Error: ' + errorMessage
replaceDict['itemTitle'] = 'Enter site information'
replaceDict['itemContent'] = body

pageTemplate = readTextFile(FILENAME_PAGE_TEMPLATE, replaceDict = replaceDict)

print "Content-Type: text/html\n\n" + pageTemplate