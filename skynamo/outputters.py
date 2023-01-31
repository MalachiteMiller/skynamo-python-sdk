import csv
from .helpers import ensureFolderExists,updateEnvironmentVariablesFromJsonConfig
def writeObjectToCsvWithObjectPropertiesAsColumnNames(object: object, filename: str, delimiter: str = ',') -> None:
	"""Writes an object to a CSV file with the object properties as column names.
	Args:
		object (object): The object to write to the CSV file.
		filename (str): The name of the CSV file to write to.
		delimiter (str): The delimiter to use when writing to the CSV file.
	"""
	ensureFolderExists('output')
	filename='output/'+filename.split('.')[0]+'.csv'
	with open(filename, 'w', newline='') as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames=object.__dict__.keys(), delimiter=delimiter,quotechar='"', quoting=csv.QUOTE_ALL)
		writer.writeheader()
		writer.writerow(object.__dict__)

def sendEmailUsingGmailCredentialsWithFilesAttached(subject: str, body: str, recipients: list[str], files: list) -> None:
	"""Sends an email using Gmail credentials with files attached.
	Args:
		subject (str): The subject of the email.
		body (str): The body of the email.
		recipient (str): The recipient of the email.
		files (list): A list of files to attach to the email.
	"""
	import smtplib
	from email.mime.multipart import MIMEMultipart
	from email.mime.text import MIMEText
	from email.mime.base import MIMEBase
	from email import encoders
	from email.mime.application import MIMEApplication

	## get sender and sender password from environment variables
	import os
	if 'SKYNAMO_GMAIL_SENDER' not in os.environ:
		updateEnvironmentVariablesFromJsonConfig()
	sender=os.environ.get('SKYNAMO_GMAIL_SENDER')
	senderPassword=os.environ.get('SKYNAMO_GMAIL_PASSWORD')
	if sender is None or senderPassword is None:
		raise Exception('SKYNAMO_GMAIL_SENDER and SKYNAMO_GMAIL_PASSWORD environment variables must be set to send emails using Gmail credentials.')
	msg = MIMEMultipart()
	msg['From'] = sender
	msg['To'] = ','.join(recipients)
	msg['Subject'] = subject
	msg.attach(MIMEText(body, 'plain'))

	for file in files:
		if 'output/' != file[:7]:
			file = 'output/'+file
		with open(file, "rb") as fil:
			part = MIMEApplication(
				fil.read(),
				Name=file.split('/')[-1]
			)
		# After the file is closed
		part['Content-Disposition'] = 'attachment; filename="%s"' % file.split('/')[-1]
		msg.attach(part)

	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(sender, senderPassword)
	text = msg.as_string()
	server.sendmail(sender, msg['To'], text)
	server.quit()