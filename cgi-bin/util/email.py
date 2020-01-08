
import smtplib
import sys

# TROUBLESHOOTING NOTE:  If the from email is a local WHB account and is not
# active or deleted, the send mail will fail with a RECEIPIENT error

#Send a mail message
def sendEmail(fromaddr, toaddrs, msg):
    try:
        try:
            server = smtplib.SMTP('localhost')
            server.set_debuglevel(0)
            server.sendmail(fromaddr, toaddrs, msg)
            server.quit()
        except smtplib.SMTPRecipientsRefused, instance:
            if (instance.recipients is not None):
                msg = str(len(instance.recipients)) + ' '
                for item in instance.recipients:
                    msg += item + '<br>'
                raise msg
            raise
    except:
        raise "Error sending mail:" + str(sys.exc_info()[0])
