#!D:/Python27/python.exe
##!/usr/bin/python

from util.html_utils import *
import cgi

form = cgi.FieldStorage()

# TODO: filter the potential people who can come in here

domain = 'ASite'
if (form.has_key('domain')):
    domain = form.getfirst('domain')

fbody = '<TABLE BORDER="0" WIDTH="600">\n'
fbody += '<TR><TD>Domain: <TD>' + createTextInput('domain', domain) + '\n'
fbody += '<TR><TD>Permanently delete: <TD>' + createCheckBox('permanent', 'True', True) + '\n'
fbody += '<TR><TD>Access Password: <TD>' + createPasswordInput('password', '') + '\n'
fbody += createSubmit('submitValue', 'Delete', 'Delete the site')

fbody += '</TABLE>'

body = '<HTML><HEAD><TITLE>Delete Site</TITLE></HEAD><BODY>' + createForm('siteForm', 'do_delete_new_site.py', 'POST', fbody) + '</BODY>'


print "Content-Type: text/html"     # HTML is following
print                               # blank line, end of headers

print body

