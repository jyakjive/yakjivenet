#!D:/Python27/python.exe
##!/usr/bin/python

from util.html_utils import *

# TODO: filter the potential people who can come in here

fbody = '<TABLE BORDER="0" WIDTH="600">\n'
fbody += '<TR><TD>Site ID<TD>' + createTextInput('siteID') + '\n'
fbody += '<TR><TD>Site CGI Dir<TD>' + createTextInput('siteCgiDir', '../../cgi-bin/yj/') + '\n'
fbody += '<TR><TD COLSPAN=2>&nbsp;\n'
fbody += '<TR><TD>Count<TD>:' + createTextInput('count', '100') + '\n'
fbody += '<TR><TD>Start at<TD>:' + createTextInput('startAt', '0') + '\n'
fbody += '<TR><TD COLSPAN=2>&nbsp;\n'
fbody += '<TR><TD>Access Password<TD>' + createPasswordInput('password', 'jezebel22') + '\n'
fbody += '<TR><TD COLSPAN="2">' + createButton('SUBMIT', 'SUBMIT', 'SUBMIT', onclick='javascript:document.forms[0].submit();', type = 'SUBMIT') + '\n'
fbody += '</TABLE>'

body = '<HTML><HEAD><TITLE>Migrate Site</TITLE></HEAD><BODY>' + createForm('siteForm', 'do_migrate_site.py', 'POST', fbody) + '</BODY>'


print "Content-Type: text/html"     # HTML is following
print                               # blank line, end of headers

print body

