import json
import uuid
import time
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order
import requests

# List all the parameters required by the task
dev_var = Variables()

dev_var.add('retrieve_cloudapp_url', var_type='String')
dev_var.add('ca_create_data', var_type='String')

context = Variables.task_call(dev_var)

#MSA_API.task_success('OK TEST',context, True)
url = context['retrieve_cloudapp_url']
payload=json.dumps(context['ca_create_data'])

headers = {
    'Authorization': 'Bearer ' + context['access_token']+'',
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)}'
}

context['headers_check']=headers


	
final_url=url
context['final_url']=final_url
response = requests.post(final_url, headers=headers,  data=payload) 
context['ca_create_response']= response.json()


try:
	json_string = json.dumps(context['ca_create_response'])
	json_object = json.loads(json_string)
	if "failed" in context['ca_create_response']:
		MSA_API.task_error(context['ca_create_response'],context, True)
	MSA_API.task_success(context['ca_create_response'],context, True)
except json.decoder.JSONDecodeError:
	MSA_API.task_error(context['ca_create_response'],context, True)



