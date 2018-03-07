#-*- coding: ASCII -*- 
import textwrap
import smtplib
from os.path import basename
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from cgi import escape
from email.header import Header
from smtplib import SMTP_SSL

class Email:
		
	def sendMail(self, fr, to, subject, text, server, cc=[]): 
		msg = MIMEMultipart('alternative')
		msg['Subject'] = subject
		msg['From'] = fr
		msg['To'] = ", ".join(to)
		msg['CC'] = ", ".join(cc)
		msg['Reply-To'] = 'REPLY EMAIL'
		#body = MIMEText(text)
		
		msg.attach(MIMEText(text, 'html'))
		    
		s = smtplib.SMTP(server)
		#s.ehlo()
		#s.starttls()
		#s.ehlo()
		#s.login('username', 'password')
		#s.ehlo()
		s.sendmail(fr, to + cc, msg.as_string())
		s.quit()
	
	
	
	
	def emailAttachment(self, fr, to, subject, text, server, files, cc=[]): #despite name only takes one file
		msg = MIMEMultipart('alternative')
		msg['Subject'] = subject
		msg['From'] = fr
		msg['To'] = ", ".join(to)
		msg['CC'] = ", ".join(cc)
		msg['Reply-To'] = 'REPLY EMAIL'
		#body = MIMEText(text)
		
		msg.attach(MIMEText(text, 'html'))
		
		with open(files, "rb") as open_file:
			attachment = MIMEApplication(open_file.read(), Name=basename(files))
			attachment['Content-Disposition'] = 'attachment; filename="%s"' % basename(files)
			msg.attach(attachment)
		    
		s = smtplib.SMTP(server)
		#s.ehlo()
		#s.starttls()
		#s.ehlo()
		#s.login('username', 'password')
		#s.ehlo()
		s.sendmail(fr, to + cc, msg.as_string())
		s.quit()


if __name__ == '__main__':
	send = sendMail('TO TEST', 'FROM TEST'.split(), 'Come to my office immediately','Found an error in GP. Need to discuss right now', 'MAIL SERVER')
	
