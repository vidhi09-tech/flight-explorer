import json
import pandas as pd
import os
from google.cloud import bigquery
from google.oauth2 import service_account

#service_account_info = json.load(open(os.environ['CONFIG_JSON']))
service_account_info = json.load(open('config.json'))
SCOPES = ['https://www.googleapis.com/auth/cloud-platform']

credentials = service_account.Credentials.from_service_account_info(
            service_account_info, scopes=SCOPES)

city = "OPO"

query = (f"""
SELECT *
FROM `basedosdados-370918.flightexplorer.baseline`
where cityOrigin = '%s'
limit 10
""" % (city))

teste = pd.read_gbq(credentials=credentials,query=query)

teste.to_csv("teste.csv")

tabela = teste.to_html()

import smtplib
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl
sender = 'rafabelokurows@gmail.com'
recipient = 'rafabelokurows@gmail.com'
#password = input(str('Enter your password: '))
app_password = os.getenv['APP_PASSWORD'] 
password = app_password #change this when pushin to Github
subject = 'Deals on airline tickets out of '+city
#body = 'Sent using Python (if it worked)'

textBefore = "<p>Hey, check out this new deals I've found for airline tickets out of "+city+".</p>This is the summary of the last run:\n"
html = textBefore + tabela

message = MIMEMultipart()
message['From'] = sender
message['To'] = recipient
message['Subject'] = subject
message.attach(MIMEText(html, 'html'))

context = ssl.create_default_context()
with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
    smtp.login(sender,password)
    smtp.sendmail(sender,recipient,message.as_string())
    
print('Email with deals sent to ',recipient)
