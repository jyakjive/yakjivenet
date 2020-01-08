#!/usr/bin/python
# email functions

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage
import smtplib
from email.Utils import COMMASPACE, formatdate
import util.exceptions

util.exceptions.handleExceptions()

lines = ''
lines =  r'<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">'
lines += r'<html xmlns="http://www.w3.org/1999/xhtml">'
lines += r'<h1>Hi!'

yourSmtp = 'mail.yakjive.com'
fromaddr = 'donotreply@yakjive.com'
password = 'YakjiveEmail2020!'
toaddrs  = ['chrisjandrews@gmail.com']

msg = MIMEMultipart('alternative')
msg['Subject'] = 'Hi'
msg['From'] = fromaddr
msg['Date'] = formatdate(localtime=True)
# Record the MIME types of both parts - text/plain and text/html.
part1 = MIMEText("text", 'plain')
part2 = MIMEText(lines, 'html')

# Attach parts into message container.
# According to RFC 2046, the last part of a multipart message, in this case
# the HTML message, is best and preferred.
msg.attach(part1)
msg.attach(part2)

server = smtplib.SMTP(yourSmtp,26)
server.set_debuglevel(0)
server.ehlo(yourSmtp)
server.starttls()
server.ehlo(yourSmtp)
server.login(fromaddr,password)
for toadd in toaddrs:
   msg['To'] = toadd
   server.sendmail(fromaddr, toadd, msg.as_string())
server.quit()