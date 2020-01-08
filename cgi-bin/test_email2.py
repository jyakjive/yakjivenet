#!/usr/bin/python

import util.email
import util.exceptions
from admin.mvc_admin import *

util.exceptions.handleExceptions()

msg = '''
From: donnotreply@yakjive.com
To: chris.j.andrews@gmail.com
Subject: Hello


Hello
'''

util.email.sendEmail('donnotreply@yakjive.com', 'chris.j.andrews@gmail.com', 'Hello')

print "Content-Type: text/html"     # HTML is following
print                               # blank line, end of headers

print '<HTML><BODY>in test email2.</BODY>'

