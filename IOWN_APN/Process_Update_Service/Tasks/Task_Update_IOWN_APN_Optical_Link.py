'''
Visit http://[YOUR_MSA_URL]/msa_sdk/ to see what you can import.
'''
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
import requests
from requests.auth import HTTPBasicAuth

dev_var = Variables()
dev_var.add('freq', var_type='String')
dev_var.add('start', var_type='Integer')
dev_var.add('end', var_type='Integer')
context = Variables.task_call(dev_var)


# API endpoint
url = "http://172.25.100.170:8080/api/v1/dags/change_subPath/dagRuns"

# Headers
headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json'
}

# Authentication
auth = HTTPBasicAuth('airflow', 'airflow')

# Payload
data = {
    "conf": {
        "freq": context['freq'],
        "start": context['start'],
        "end": context['end']
    }
}

# Making the POST request
#response = requests.post(url, headers=headers, auth=auth, json=data)

response = 200

# Printing the response
#print(f"Status Code: {response.status_code}")
#print(f"Response Body: {response.text}")

#if response.status_code == 200:
if response == 200:
	ret = MSA_API.process_content('ENDED', 'Task OK', context, True)
else:
	ret = MSA_API.process_content('FAILED', 'Task Failed', context, True)
print(ret)

