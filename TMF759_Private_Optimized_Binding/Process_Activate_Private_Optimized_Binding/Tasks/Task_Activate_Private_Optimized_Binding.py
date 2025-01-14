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
dev_var.add('get_ue_url_path', var_type='String')
dev_var.add('ue_id', var_type='String')
dev_var.add('ca_id', var_type='String')
context = Variables.task_call(dev_var)

#MSA_API.task_success('OK TEST',context, True)
url = context['tmf759_url']+''+context['get_ue_url_path']+'/'+context['ue_id']

ue_id=context['ue_id']
ca_id=context['ca_id']

data={
  "id": ue_id,
  "activationFeature": [
    {
      "id": "1",
      "isEnabled": True,
      "name": "privateOptimizedBindingFeature",
      "featureCharacteristic": [
        {
          "name": "privateOptimizedBindingCloudAppHref",
          "value": "https://tmf759-catalyst-dev.nprd-gw.cloud.att.com/pob/v1/cloudApplication/"+ca_id,
          "@type": "StringCharacteristic"
        },
        {
          "name": "metric",
          "value": "udp_tp_class_ul[5m]",
          "@type": "StringCharacteristic"
        }
      ],
      "@type": "BindingFeature"
    }
  ],
  "@type": "UserEquipment"
}
context['dataCheck']=data
payload = json.dumps(data)

headers = {
    'Authorization': 'Bearer ' + context['access_token']+'',
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)}',
    'X-ATT-ClientId': ''+context['client_id']+''
}

'''
headers = {
    'Authorization': 'Bearer ' + context['access_token']+'',
    'Content-Type': 'application/json',
    'X-ATT-ClientId': ''+context['client_id']+''
}
'''
context['headers_check']=headers

final_url=url

time.sleep(8)

context['final_url']=final_url
response = requests.patch(final_url, headers=headers, data=payload) 
#context['cr_video_camera_url_response']= str(response)
context['cr_video_camera_url_response']= response.json()
#context['cr_video_camera_url_response']= response

try:
	json_string = json.dumps(context['cr_video_camera_url_response'])
	json_object = json.loads(json_string)
	if "failed" in context['cr_video_camera_url_response']:
		MSA_API.task_error(context['cr_video_camera_url_response'],context, True)
	json_response = json.dumps(context['cr_video_camera_url_response'], indent=4)
	MSA_API.task_success(json_response,context, True)
except json.decoder.JSONDecodeError:
	MSA_API.task_error(context['cr_video_camera_url_response'],context, True)