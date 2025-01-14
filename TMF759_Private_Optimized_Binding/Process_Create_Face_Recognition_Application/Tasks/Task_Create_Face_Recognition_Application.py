import json
import uuid
import time
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order
import requests

# List all the parameters required by the task
dev_var = Variables()
dev_var.add('tmf759_url', var_type='String')
dev_var.add('get_ca_url_path', var_type='String')
context = Variables.task_call(dev_var)

url = context['tmf759_url']+''+context['get_ca_url_path']

data={
  "id": "",
  "href": "",
  "operationalState": "enable",
  "name": "Face Recognition Application",
  "note": [
    {
      "text": "Stadium Security Department Face Recognition Application",
      "@type": "Note"
    }
  ],
  "resourceCharacteristic": [
    {
      "name": "cloudProvider",
      "value": "Azure",
      "@type": "StringCharacteristic"
    },
    {
      "name": "cloudRegion",
      "value": "eastus",
      "@type": "StringCharacteristic"
    },
    {
      "name": "cloudReference",
      "value": "/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/vnet-rg/providers/Microsoft.Compute/example",
      "@type": "StringCharacteristic"
    }
  ],
  "@type": "CloudApplication",
  "@schemaLocation": "http://tmf759-catalyst-dev.nprd-gw.cloud.att.com/CloudApplication.schema.json",
  "@baseType": "LogicalResource"
}

payload = json.dumps(data)


headers = {
    'Authorization': 'Bearer ' + context['access_token']+'',
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)}',
    'X-ATT-ClientId': ''+context['client_id']+''
}

context['headers_check']=headers


	
final_url=url
	
context['final_url']=final_url
response = requests.post(final_url, headers=headers, data=payload) 
#context['cr_face_rec_app_url_response']= str(response)
context['cr_face_rec_app_url_response']= response.json()
#context['cr_face_rec_app_url_response']= response

try:
	json_string = json.dumps(context['cr_face_rec_app_url_response'])
	json_object = json.loads(json_string)
	if "failed" in context['cr_face_rec_app_url_response']:
		MSA_API.task_error(context['cr_face_rec_app_url_response'],context, True)
	
	context['ca_id']=context['cr_face_rec_app_url_response']["id"]
	json_response = json.dumps(context['cr_face_rec_app_url_response'], indent=4)
	MSA_API.task_success(json_response,context, True)
except json.decoder.JSONDecodeError:
	MSA_API.task_error(context['cr_face_rec_app_url_response'],context, True)