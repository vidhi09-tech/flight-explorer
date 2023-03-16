import json
import pandas as pd
import os
from google.cloud import bigquery
from google.oauth2 import service_account

#service_account_info = json.load(open(os.environ['CONFIG_JSON']))
service_account_info = json.load(open('config.json'])
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
