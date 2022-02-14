#!/usr/bin/python3
import smtplib
import argparse
import logging
import sys

FORMAT = '%(asctime)s %(name)s %(levelname)s: %(message)s'

EPILOG = '''\ 
Text message via email:

T-Mobile – number@tmomail.net
Virgin Mobile – number@vmobl.com
AT&T – number@txt.att.net
Sprint – number@messaging.sprintpcs.com
Verizon – number@vtext.com
Tracfone – number@mmst5.tracfone.com
Ting – number@message.ting.com
Boost Mobile – number@myboostmobile.com
U.S. Cellular – number@email.uscc.net
Metro PCS – number@mymetropcs.com
'''

def usage():
    print("-u  | --user:   email account address   --user <sender>@gmail.com required = True")
    print("-pw | --passwd  email password  --passwd <password for email account>  required = True")
    print("-t  | --to      email send to   --to <reciever>@gmail.com required = True")
    print("-su | --subject email subject   --subject <title>  default Lanforge Report default = Lanforge Report")
    print("-b  | --body    email body      --body <body text> required = True")
    print("-s  | --smtp    smtp server     --smtp <smtp server>  default  smtp.gmail.com  default=smtp.gmail.com")
    print("-p  | --port    smtp port       --port <port>  default 465 (SSL)  default=465")

# see https://stackoverflow.com/a/13306095/11014343
class FileAdapter(object):
    def __init__(self, logger):
        self.logger = logger
    def write(self, data):
        # NOTE: data can be a partial line, multiple lines
        data = data.strip() # ignore leading/trailing whitespace
        if data: # non-blank
           self.logger.info(data)
    def flush(self):
        pass  # leave it to logging to flush properly

def main():

    parser = argparse.ArgumentParser(description="lanforge email",epilog=EPILOG,
    formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-u", "--user",      type=str, help="email account   --user <sender>@gmail.com", required = True)
    parser.add_argument("-pw", "--passwd",   type=str, help="email password  --passwd <password for email account>", required = True)
    parser.add_argument("-t", "--to",        type=str, help="email send to   --to <reciever>@gmail.com", required = True)
    parser.add_argument("-su", "--subject",  type=str, help="email subject   --subject <title>  default Lanforge Report", default="Lanforge Report")
    parser.add_argument("-b", "--body",      type=str, help="email body      --body <body text>", required = True)
    parser.add_argument("-s,", "--smtp",     type=str, help="smtp server     --smtp <smtp server>  default  smtp.gmail.com ", default="smtp.gmail.com")
    parser.add_argument("-p,", "--port",     type=str, help="smtp port       --port <port>  default 465 (SSL)", default="465")
    parser.add_argument("-l", "--log",       type=str, help="logfile for messages, stdout means output to console",default="stdout")


    args = None
    try:
       args = parser.parse_args()
       logfile = args.log
    except Exception as e:
      print(e)
      usage()
      exit(2)        
   
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter(FORMAT)
    logg = logging.getLogger(__name__)
    logg.setLevel(logging.DEBUG)
    file_handler = None
    if (logfile is not None):
       if (logfile != "stdout"):
           file_handler = logging.FileHandler(logfile, "w")

           file_handler.setLevel(logging.DEBUG)
           file_handler.setFormatter(formatter)
           logg.addHandler(file_handler)
           logg.addHandler(logging.StreamHandler(sys.stdout)) # allows to logging to file and stderr
       else:
           # stdout logging
           logging.basicConfig(format=FORMAT, handlers=[console_handler])
    try:
        email_text = 'Subject: {}\n\n{}'.format(args.subject, args.body )
        server = smtplib.SMTP_SSL(args.smtp, int(args.port))
        server.ehlo()
        server.login(args.user,args.passwd)
        server.sendmail(args.user, args.to, email_text)
        server.close()

        logg.info('email Sent!  smtp server: {} port: {}'.format(args.smtp, args.port))
    except:
        logg.info('email failed')
        logg.info("Is access for less secure apps setting has been turned on for the email account?")

# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
if __name__ == '__main__':
    main()
    print("Lanforge send email via smtp server")
