from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
# from builtins import *
import smtplib
import warnings

class GmailContentObject:
    def __init__(self,subject,body,credentials):
        self.subject = subject
        self.body = body
        if not credentials:
            raise AttributeError("credential is missing")
        self.credentials = credentials
    def deliver(self,recipient_email):
        sender_email = self.credentials['sender_gmail_addr']
        sender_gmail_pwd = self.credentials['sender_gmail_pwd']
        success,error_msg = True,None
        try:
            EMAIL_ADDRESS = sender_email
            PASSWORD = sender_gmail_pwd
            server = smtplib.SMTP('smtp.gmail.com:587')
            server.ehlo()
            server.starttls()
            server.login(EMAIL_ADDRESS,PASSWORD)
            message = "Subject: {}\n\n{}".format(self.subject,self.body)
            server.sendmail(EMAIL_ADDRESS,recipient_email,message)
            server.quit()
            # print("Email success")
        except Exception as e:
            # print("Email failed: {}".format(e))
            error_msg = format(e)
            success = False
            warnings.warn("Error in sending mail:{}".format(error_msg))
        return success,error_msg
        



class SimpleGmailService:
    def __init__(self,sender_gmail_addr=None,sender_gmail_pwd=None):
        if sender_gmail_addr:
            self.sender_gmail_addr = sender_gmail_addr
            if sender_gmail_pwd:
                self.sender_gmail_pwd = sender_gmail_pwd
            else:
                raise AttributeError("sender gmail password is missing")
        else:
            self.__use_default_credentials__()
    def create_mail(self,subject,message):
        credentials = {}
        credentials['sender_gmail_addr'] = self.sender_gmail_addr
        credentials['sender_gmail_pwd'] = self.sender_gmail_pwd
        if not subject:
            raise AttributeError("subject cannot be None")
        if not message:
            raise AttributeError("message cannot be None")
        gmailObject = GmailContentObject(subject,message,credentials)
        return gmailObject



    def __use_default_credentials__(self):
        self.sender_gmail_addr = 'rock307977586@gmail.com'
        self.sender_gmail_pwd = 'qotojtrnfgwenhsd' # temporary publickey


def send_email(sub,msg):
  try:
    EMAIL_ADDRESS = 'rock307977586@gmail.com'
    PASSWORD = 'qotojtrnfgwenhsd'
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(EMAIL_ADDRESS,PASSWORD)
    message = "Subject: {}\n\n{}".format(sub,msg)
    server.sendmail(EMAIL_ADDRESS,"307977586@qq.com",message)
    server.quit()
    print("Email success")
  except Exception as e:
    print("Email failed: {}".format(e))

if __name__ == "__main__":
    gmailService = SimpleGmailService()
    mail = gmailService.create_mail("some subject","some content")
    mail.deliver("someone@domain.com")