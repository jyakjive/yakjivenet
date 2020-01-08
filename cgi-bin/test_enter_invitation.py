#!/usr/bin/python
##!C:/apps/python24/python.exe

from util.html_utils import *

# TODO: filter the potential people who can come in here

fbody = '<TABLE BORDER="0" WIDTH="600">\n'
fbody += '<TR><TD>Invitation code: <TD> ' + createTextInput('inviteCode') + '\n'
fbody += '<TR><TD COLSPAN="2">' + createButton('SUBMIT', 'SUBMIT', 'SUBMIT', type = 'SUBMIT') + '\n'

fbody += '</TABLE>'

body = '<HTML><HEAD><TITLE>Enter Invitation Code</TITLE></HEAD><BODY>' + createForm('siteForm', 'remove_new_site.py', 'POST', fbody) + '</BODY>'


print "Content-Type: text/html"     # HTML is following
print                               # blank line, end of headers

print body

