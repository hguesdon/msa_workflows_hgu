import json
import uuid
import time
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order
import requests

# List all the parameters required by the task
dev_var = Variables()

dev_var = Variables()
dev_var.add('tmf759_url', var_type='String')
dev_var.add('get_ca_url_path', var_type='String')
context = Variables.task_call(dev_var)

#MSA_API.task_success('OK TEST',context, True)
url = context['tmf759_url']+''+context['get_ca_url_path']


headers = {
    'Authorization': 'Bearer ' + context['access_token']+'',
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)}',
    'X-ATT-ClientId': ''+context['client_id']+''
}

context['headers_check']=headers

final_url=url
context['final_url']=final_url
response = requests.get(final_url, headers=headers) 
context['ca_list_response']=[]
#context['ca_list_response']= str(response)
context['ca_list_response']= response.json()


try:
	json_string = json.dumps(context['ca_list_response'])
	json_object = json.loads(json_string)
	if "failed" in context['ca_list_response']:
		MSA_API.task_error(context['ca_list_response'],context, True)
	if not context['ca_list_response']:
		MSA_API.task_error("Cloud Application Information not found : "+str(context['ca_list_response']),context, True)
	else:
		MSA_API.task_success(context['ca_list_response'],context, True)
except json.decoder.JSONDecodeError:
	MSA_API.task_error(context['ca_list_response'],context, True)



