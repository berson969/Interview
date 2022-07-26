import email
import os
from smtplib import SMTP
from imaplib import IMAP4_SSL
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

GMAIL_SMTP = "smtp.gmail.com"
GMAIL_IMAP = "imap.gmail.com"


class EmailPolicy:
    def __init__(self, our_email, _password, _header=None):
        self.our_email = our_email
        self.password = _password
        self.header = _header


class EmailSender(EmailPolicy, MIMEMultipart):
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def sending(self, recipients, subject='Subject', message='Message'):
        self.message['From'] = self.our_email
        self.message['To'] = ', '.join(recipients)
        self.message['Subject'] = subject
        self.message.attach(message)
        # identify ourselves to smtp gmail client
        self.ehlo()
        # secure our email with tls encryption
        self.starttls()
        # re-identify ourselves as an encrypted connection
        self.ehlo()
        self.login(self.our_email, self.password)
        self.sendmail(self.our_email, self, self.message.as_string())
        self.quit()
        return True


class EmailReciever(EmailPolicy, IMAP4_SSL):
    def __init__(self, host):
        self.host = host

    def recieve_email(self):
        self.login(self.our_email, self.password)
        self.list()
        self.select("inbox")
        self.criterion = '(HEADER Subject "%s")' % self.header if self.header else 'ALL'
        result, data = self.uid('search', None, self.criterion)
        assert data[0], 'There are no letters with current header'
        latest_email_uid = data[0].split()[-1]
        result, data = self.uid('fetch', latest_email_uid, '(RFC822)')
        raw_email = data[0][1]
        self.recieved_message = email.message_from_string(raw_email)
        self.logout()
        return self.recieved_message


if __name__ == '__main__':
    load_dotenv('.env')
    mail_client = EmailPolicy(os.getenv('LOGIN'), os.getenv('PASSWORD'))
    send_email = EmailSender(GMAIL_SMTP, 587)
    send_email.sending(['vasya@email.com', 'petya@email.com'])
    check_email = EmailReciever(GMAIL_IMAP)
    text_from_email = check_email.recieve_email()

# l = 'login@gmail.com'
# passwORD = 'qwerty'
# subject = 'Subject'
# recipients = ['vasya@email.com', 'petya@email.com']
# message = 'Message'
# header = None

# send message
# msg = MIMEMultipart()
# msg['From'] = l
# msg['To'] = ', '.join(recipients)
# msg['Subject'] = subject
# msg.attach(MIMEText(message))

# ms = smtplib.SMTP(GMAIL_SMTP, 587)
# # identify ourselves to smtp gmail client
# ms.ehlo()
# # secure our email with tls encryption
# ms.starttls()
# # re-identify ourselves as an encrypted connection
# ms.ehlo()
#
# ms.login(l, passwORD)
# ms.sendmail(l,
# ms, msg.as_string())
#
# ms.quit()
# send end


# recieve
# mail = imaplib.IMAP4_SSL(GMAIL_IMAP)
# mail.login(l, passwORD)
# mail.list()
# mail.select("inbox")
# criterion = '(HEADER Subject "%s")' % header if header else 'ALL'
# result, data = mail.uid('search', None, criterion)
# assert data[0], 'There are no letters with current header'
# latest_email_uid = data[0].split()[-1]
# result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
# raw_email = data[0][1]
# email_message = email.message_from_string(raw_email)
# mail.logout()
# #end recieve
