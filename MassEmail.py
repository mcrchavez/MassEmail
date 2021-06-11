#Use for mass automated emailing with login
import email , smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio

import sys
import argparse
from typing import SupportsRound


#MIMEMultipart object has sub classes with different media types

"""
MIMEText — Plain text, this will make up the body of our email.
MIMEImage — Allows us to add images to our email.
MIMEAudio — Audio files are added with this part.
MIMEApplication — Any other attachments can be added with this.
"""


class Email:
    def __init__(self, email_addr='', email_domain='@gmail.com', passw= '', attrib = None):
        self.email_addr = email_addr
        self.email_domain = email_domain 
        self.passw = passw
        self.attrib = attrib


    def characteristics(self):
        return_dict = dict()
        return_dict['Email:'] = str(self.email_addr + self.email_domain)
        return_dict['Password:'] = str(self.passw)
        return_dict['Attributes:'] = self.attrib
        return return_dict
    def __str__(self):
        return_str = '-'*35 + '\n'
        vals = self.characteristics()
        
        for key, val in vals.items():
            if val != None:
                return_str += str(key) + ' ' + str(val)
            else:
                return_str += str(key) + ' ' +  'N/A'
            return_str += '\n'
        return_str += '-'*35 + '\n'
        return return_str

    def get_address(self):
        return str(self.email_addr + self.email_domain)
    
    def set_attribute(self, is_valid):
        self.attrib = is_valid


class Send_mail:
    def __init__(self, sender, receivers = [], subject='', body_txt='', images=None, smtp_server=('smtp.gmail.com', 587)): 
        """Void Type

        sender is an Email object
        recievers is a dictionary of Email objects
        subject will become subject line of emails to be sent via MIME object
        images 
        """
        self.sender = sender
        self.receivers = receivers
        self.subject = subject
        self.body_text = body_txt 
        self.images = images
        self.smtp_server = smtp_server

    def characteristics(self):
        #dict of object attributes
        return_dict = dict()
        return_dict['Sender:'] = str(self.sender).strip('-')
        #reciever list
        rec_ls = []
        for item in self.receivers:
            if type(item) == str:
                rec_ls.append(item)
            else:
                rec_ls.append(item.email_addr + item.email_domain)
            
        return_dict["Receivers:"] = rec_ls
        return_dict["Subject:"] = str(self.subject)
        return_dict["Body:"] = self.body_text
        return return_dict
    def __str__(self):
        return_str = '-'*35 + '\n'
        for key, val in self.characteristics().items():
            if val != None:
                return_str += str(key) + ' ' + str(val)
            else:
                return_str += str(key) + ' ' +  'N/A'
            return_str += '\n'
        return_str += '-'*35 + '\n'
        return return_str

    def set_sender(self, email_obj=''):
        self.sender = email_obj

    def set_receivers(self, receivers=[]):
        self.receivers = receivers
    
    def add_receiver(self, email_obj):
      
        self.receivers.append(email_obj)

    def send_email(self):
        
        search_dict = self.characteristics()
        curr_email = ''
        for item in search_dict["Receivers:"]:
            try:
                curr_email = item
                email = MIMEMultipart()
                email["From"] = self.sender.get_address()
                email["To"] = item
                email["Subject"] = self.subject
                password = self.sender.passw
                #attaches text to email object with plaintext type
                email.attach(MIMEText(self.body_text, "plain"))
                #start the smtp session
                #connect to the gmail smtp server using the tcp 587 port 
                #start a tls session 
                session = smtplib.SMTP(self.smtp_server[0], self.smtp_server[1])
                session.starttls()

                #login to session via smtp server with sender address and password
                session.login(self.sender.get_address(), password) 
                self.sender.set_attribute(True)
                text = email.as_string()
                print("sending to " + item + '...')
                session.sendmail(self.sender.get_address(), item, text)
                session.quit()
                print('Mail Sent From: ' + self.sender.get_address() + ' To: ' + item)
            except smtplib.SMTPAuthenticationError:
                #catch authentication error if email login is incorrect
                print("sender email username or password invalid")
                self.sender.set_attribute(False)
            except smtplib.SMTPRecipientsRefused:
                #catch error if recipient Email object refused connection
                print("recipient address invalid")

arg_parser = argparse.ArgumentParser(description="Python framework for automated email phishing")

# uses "store" action which just attaches stored value to -d in argparse
define_sub_commands = arg_parser.add_subparsers(description="Set source email info and target email addresses")

source_parser = define_sub_commands.add_parser("-S", help="Set email info")
source_parser.add_argument("-d", "--address", help="Set email domain ex. email@gmail.com")
#source_parser.add_argument(["-p", "--password"], help="Set password for source email login", required=True)

target_parser = define_sub_commands.add_parser("-T", help="Set target addresses via file or through cmdline")
target_parser.add_argument("-t", "--target",nargs="*", help="Enter target email addresses ex. email@gmail.com email2@gmail.com")
#target_parser.add_argument(["-tf", "--file"], nargs="?", help="Provide csv text file for target email addresses")


def main():
    try:
        #skip the first arg which is MassEmail.py in cmdline
        args = arg_parser.parse_args((sys.argv[1:]))
    except argparse.ArgumentError as e:
        print("Error")
    


if __name__=="__main__":
    main()