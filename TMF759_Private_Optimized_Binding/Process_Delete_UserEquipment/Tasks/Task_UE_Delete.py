import json
import uuid
import time
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order
import requests

# List all the parameters required by the task
dev_var = Variables()

dev_var.add('retrieve_ue_url', var_type='String')
dev_var.add('ue_update_id', var_type='String')

context = Variables.task_call(dev_var)

#MSA_API.task_success('OK TEST',context, True)
url = context['retrieve_ue_url']

headers = {
    'Authorization': 'Bearer ' + context['access_token']+'',
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)}'
}

context['headers_check']=headers

if "ue_update_id" not in context or not context['ue_update_id']:
	context['ue_update_id']=''
	
final_url=url+context['ue_update_id']
	
context['final_url']=final_url
response = requests.delete(final_url, headers=headers) 
context['ue_delete_response']= response.json()


try:
	json_string = json.dumps(context['ue_delete_response'])
	json_object = json.loads(json_string)
	if "failed" in context['ue_delete_response']:
		MSA_API.task_error(context['ue_delete_response'],context, True)
	MSA_API.task_success(context['ue_delete_response'],context, True)
except json.decoder.JSONDecodeError:
	MSA_API.task_error(context['ue_delete_response'],context, True)



