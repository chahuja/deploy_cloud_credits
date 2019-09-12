"""
Usage: python server.py -csv <file-to-gcp_codes> -port 7000 -code GCP -FROM <your-andrew-id>

Example: python server.py -csv ../codes/gcp2019codes.csv -port 7000 -code GCP -FROM cahuja
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from csv2dict import read_codes

from http.server import SimpleHTTPRequestHandler
import socketserver

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import csv
import datetime

import sys
sys.path.append('..')

import getpass
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-csv', type=str,
                    help='csvfile')
parser.add_argument('-port', type=int,
                    help='pklfile')
parser.add_argument('-code', type=str,
                    help='GCP or AWS')
parser.add_argument('-FROM', type=str,
                    help='your andrew id')
args = parser.parse_args()

USERNAME=args.FROM
PASSWORD= getpass.getpass('Enter andrew passwd for {}: '.format(USERNAME)) #sec.pss()


class Email:
    def __init__(self, f, codes):
        self.logger = f
        self.codes = codes

    def _connect(self):
        self.server = smtplib.SMTP('smtp.andrew.cmu.edu', 587)
        self.server.starttls()
        self.server.login(USERNAME,PASSWORD)

    def send_email(self, post_data):
        first, last, andrew = post_data.decode("utf-8").split('&')
        first = first.split('=')[1]
        last = last.split('=')[1]
        andrew = andrew.split('=')[1]
        if andrew not in self.codes: 
            self.logger.write('FAIL: %s\t%s\t%s %s\n' % (datetime.datetime.now(),andrew,first,last))
            self.logger.flush()
            return 'Error!\n\nMake sure your andrew id is correct. If problem persists contact {}@andrew.cmu.edu'.format(args.FROM)
        msg = MIMEMultipart()
        msg['From'] = '{}@andrew.cmu.edu'.format(args.FROM)
        msg['To'] = andrew+'@andrew.cmu.edu'
        msg['Subject'] = "$50 {} Code for 11777".format(args.code)
        body = 'Dear {} {},\n\nYour {} code(s) are {}.\n\nBest,\n11777 Instructors'.format(first, last, args.code, self.codes[andrew])
        msg.attach(MIMEText(body, 'plain'))
        self._connect()
        self.server.sendmail('{}@andrew.cmu.edu'.format(args.FROM), andrew+'@andrew.cmu.edu', msg.as_string())
        self.terminate()
        self.logger.write('SUCCESS: %s\t%s\t%s %s\n' % (datetime.datetime.now(),andrew,first,last))
        self.logger.flush()
        return 'Success! Check your email for the code.'

    def _test_status(self):
        try:
            status = self.server.noop()[0]
        except:
            status = -1
        if status != 250: self._connect()

    def terminate(self):
        self.server.quit()

class AndrewHandler(SimpleHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        status = self.server.email.send_email(post_data)
        self._set_headers()
        self.wfile.write("<html><body><font size=\"4\">{}</font></body></html>".format(status).encode("utf-8"))

codes = read_codes(args.csv)
f = open('logger.txt','a')
emailer = Email(f, codes)

PORT = args.port
Handler = AndrewHandler
httpd = socketserver.TCPServer(("", PORT), Handler)
httpd.email = emailer

print("serving at port", PORT)
httpd.serve_forever()
f.close()
httpd.email.terminate()
