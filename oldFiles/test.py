import json
import pandas as pd
import os
from google.cloud import bigquery
from google.oauth2 import service_account
import base64

key = os.getenv('GCP_PRIVATE_KEY')
key_b64 = base64.b64encode(key.encode())
key_decoded = base64.b64decode(key_b64).decode()
project = os.getenv('GCP_PROJECT_ID')
project_b64 = base64.b64encode(project.encode())
project_decoded = base64.b64decode(project_b64).decode()
clientid = os.getenv('GCP_CLIENT_ID')
client_b64 = base64.b64encode(clientid.encode())
client_decoded = base64.b64decode(client_b64).decode()


service_account_info = {
  "type": "service_account",
  "project_id": "project",
  "private_key_id": "34da29e1c968cf2bd1e5d16a47d5ea8030b90d7f",
  "private_key": "-----BEGIN PRIVATE KEY-----\nkey\n-----END PRIVATE KEY-----\n",
  "client_email": "teste-11@basedosdados-370918.iam.gserviceaccount.com",
  "client_id": "client",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/teste-11%40basedosdados-370918.iam.gserviceaccount.com"
}
service_account_info["private_key"] = service_account_info["private_key"].replace("key", key_decoded).replace("\\n", "\n")
service_account_info["project_id"] = service_account_info["project_id"].replace("project", project_decoded).replace("\\n", "\n")
service_account_info["client_id"] = service_account_info["client_id"].replace("client", client_decoded).replace("\\n", "\n")

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
app_password = os.getenv('APP_PASSWORD')
password = app_password #change this when pushin to Github
subject = 'Deals on airline tickets out of '+city

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
