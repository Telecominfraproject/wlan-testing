#!/usr/bin/env python3
import smtplib
from email.message import EmailMessage
import sys

def writeEmail(emailBody):
	msg = EmailMessage()
	msg.set_content(emailBody)
	return msg


def sendEmail(email, sender, recipient, subject, smtpServer='localhost'):
	email['Subject'] = subject
	email['From'] = sender
	email['To'] = recipient

	try:
		s = smtplib.SMTP(smtpServer)
		s.send_message(email)
		s.quit()
		return True
	except Exception as e:
		print("Send Failed, {}".format(e))
		sys.exit(2)





#body = "Hello This Is A Test"
#subject = "Test Email"
#recipient = "logan.lipke@candelatech.com"
#sender = "lanforge@candelatech.com"

#email = writeEmail(body)

#sendEmail(email, sender, recipient, subject)
