#!/usr/bin/python3

import argparse
import json
import sys
import os
import traceback
import smtplib
from email.mime.text import MIMEText

"""
usage: python3 send_email_notification.py [-h] [--config CONFIG] [--subject SUBJECT] [--body BODY] [--sender SENDER] [--receiver RECEIVER]

Tool to send email notification.

optional arguments:
    -h, --help                show this help message and exit
    -c CONFIG, --config CONFIG    The email configuration file. Default is "/home/secrets/pdbihm/mail.json"
    -s SUBJECT, --subject    The email subject. Default is "PDB WWW Backups Error"
    -b BODY, --body BODY    The file with the message body. Default is "/home/pdbihm/backup_logs/data-aws.pdb-dev.org/error.log"
    -r SENDER, --sender SENDER    The sender of the email. Default is "PDB-DEV Online Notification <no-reply@pdb-dev.org>"
    -d RECEIVER, --receiver RECEIVER    The receiver of the email. Default is pdb-ihm@wwpdb.org.                           
"""

parser = argparse.ArgumentParser(description='Tool to send email notifications.')
parser.add_argument( '-c', '--config', help='The mail configuration file.', action='store', type=str, default='/home/secrets/pdbihm/mail.json')
parser.add_argument( '-s', '--subject', help='The mail subject.', action='store', type=str, default='PDB WWW Backups Error')
parser.add_argument( '-b', '--body', help='The file with the mail body.', action='store', type=str, default='/home/pdbihm/backup_logs/data-aws.pdb-dev.org/error.log')
parser.add_argument( '-r', '--sender', help='The mail sender.', action='store', type=str, default='PDB-DEV Online Notification <no-reply@pdb-dev.org>')
parser.add_argument( '-d', '--receiver', help='The mail receiver.', action='store', type=str, default='pdb-ihm@wwpdb.org')

args = parser.parse_args()
#print(f'config={args.config}\nsubject={args.subject}\nbody={args.body}\nsender={args.sender}\nreceiver={args.receiver}')
f = open(args.body, 'r')
body = f.read()
f.close()

if not os.path.isfile(args.config):
    print('email configuration file must exist.')
    sys.exit(1)

with open(args.config, 'r') as f:
    config = json.load(f)

#print(json.dumps(config, indent=4))

mail_footer = config['footer']
mail_server = config['server']
mail_port = config['port']
mail_sender = config['sender']
mail_receiver = args.receiver
user = config['user']
password = config['password']
subject = args.subject


msg = MIMEText('%s\n\n%s' % (body, mail_footer), 'plain')
msg['Subject'] = subject
msg['From'] = mail_sender
msg['To'] = mail_receiver
try:
    #print(f'Connecting to {mail_server}:{mail_port}.')
    s = smtplib.SMTP_SSL(mail_server, mail_port)
    #print('Logging...')
    s.login(user, password)
    #print(f'Sending from {mail_sender} to {mail_receiver}.')
    s.sendmail(mail_sender, mail_receiver.split(','), msg.as_string())
    #print('Quiting...')
    s.quit()
    #print('The test email was sent.')
except:
    et, ev, tb = sys.exc_info()
    print('got exception "%s"' % str(ev))
    print('%s' % ''.join(traceback.format_exception(et, ev, tb)))

