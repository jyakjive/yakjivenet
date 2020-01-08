#!D:/Python27/python.exe
##!/usr/bin/python

from util.html_utils import *

# TODO: filter the potential people who can come in here

fbody = '<TABLE BORDER="0" WIDTH="600">\n'
fbody += '<TR><TD>domain<TD>' + createTextInput('domain', 'ASite') + '\n'
fbody += '<TR><TD>siteTitle<TD>' + createTextInput('siteTitle', 'Test Site') + '\n'
fbody += '<TR><TD>siteSubTitle<TD>' + createTextInput('siteSubTitle', 'This is a test site') + '\n'
fbody += '<TR><TD>siteCategory<TD>' + createTextInput('siteCategory', 'Enter category here') + '\n'
fbody += '<TR><TD>metaKeywords<TD>' + createTextInput('metaKeywords', 'Enter keywords here') + '\n'
fbody += '<TR><TD>metaDescription<TD>' + createTextInput('metaDescription', 'Enter description here') + '\n'
fbody += '<TR><TD>webmasterNickname<TD>' + createTextInput('webmasterNickname', 'TestUser') + '\n'
fbody += '<TR><TD>webmasterUsername<TD>' + createTextInput('webmasterUsername', 'testuser') + '\n'
fbody += '<TR><TD>webmasterPassword<TD>' + createTextInput('webmasterPassword', 'test1234') + '\n'
fbody += '<TR><TD>webmasterFirst<TD>' + createTextInput('webmasterFirst', 'Test') + '\n'
fbody += '<TR><TD>webmasterLast<TD>' + createTextInput('webmasterLast', 'Test') + '\n'
fbody += '<TR><TD>companyName<TD>' + createTextInput('companyName', 'Test company') + '\n'
fbody += '<TR><TD>webmasterEmail<TD>' + createTextInput('webmasterEmail', 'test@test.test') + '\n'
fbody += '<TR><TD>webmasterKey<TD>' + createTextInput('webmasterKey', '124567890abcdefghijk') + '\n'
fbody += '<TR><TD>rootURL<TD>' + createTextInput('rootURL', 'www.newscommunity.net') + '\n'

fbody += '<TR><TD>Access Password<TD>' + createPasswordInput('password', '') + '\n'
fbody += '<TR><TD COLSPAN="2">' + createSubmit('SUBMIT', 'Create my site', 'Click to create your site') + '\n'

fbody += '</TABLE>'

body = '<HTML><HEAD><TITLE>Add site</TITLE></HEAD><BODY>' + createForm('siteForm', 'create_new_site.py', 'POST', fbody) + '</BODY>'


print "Content-Type: text/html"     # HTML is following
print                               # blank line, end of headers

print body

