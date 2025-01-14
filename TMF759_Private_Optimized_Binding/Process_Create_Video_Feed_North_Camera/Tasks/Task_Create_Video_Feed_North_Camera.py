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
dev_var.add('ue_imsi', var_type='String')
dev_var.add('ue_msisdn', var_type='String')
dev_var.add('ue_ipv4Address', var_type='String')
dev_var.add('camera', var_type='String')
context = Variables.task_call(dev_var)

#MSA_API.task_success('OK TEST',context, True)
url = context['tmf759_url']+''+context['get_ue_url_path']

if context['camera'] == "camera1":
	context['ue_imsi']="311180001300001"
	context['ue_ipv4Address']="10.33.57.4"
	context['ue_msisdn']="1001300001"

if context['camera'] == "camera2":
	context['ue_imsi']="311180001300002"
	context['ue_ipv4Address']="10.33.57.5"
	context['ue_msisdn']="1001300002"
	
ue_imsi=context['ue_imsi']
ue_ipv4Address=context['ue_ipv4Address']
ue_msisdn=context['ue_msisdn']
data={
  "id": "",
  "href": "",
  "description": "Streaming Video Footage North Camera",
  "name": "Stadium Security North Camera",
  "operationalState": "enable",
  "note": [
    {
      "text": "Stadium Security Department Real Time Video Feed North Camera",
      "@type": "Note"
    }
  ],
  "place": [
    {
      "id": "9912",
      "href": "https://host:port/geographicAddressManagement/v5/geographicAddress/9912",
      "role": "Area",
      "place": {
        "locality": "Brussels",
        "streetNrLast": "100",
        "streetSuffix": "North"
      },
      "@type": "PlaceRef",
      "@referredType": "GeographicAddress"
    }
  ],
  "resourceCharacteristic": [
    {
      "name": "msisdn",
      "value": ue_msisdn,
      "@type": "StringCharacteristic"
    },
    {
      "name": "imsi",
      "value": ue_imsi,
      "@type": "StringCharacteristic"
    },
    {
      "name": "ipv4Address",
      "value": ue_ipv4Address,
      "@type": "StringCharacteristic"
    }
  ],
  "@type": "UserEquipment",
  "@schemaLocation": "http://tmf759-catalyst-dev.nprd-gw.cloud.att.com/UserEquipment.schema.json",
  "@baseType": "PhysicalResource"
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
#context['cr_video_camera_url_response']= str(response)
context['cr_video_camera_url_response']= response.json()
#context['cr_video_camera_url_response']= response

try:
	json_string = json.dumps(context['cr_video_camera_url_response'])
	json_object = json.loads(json_string)
	if "failed" in context['cr_video_camera_url_response']:
		MSA_API.task_error(context['cr_video_camera_url_response'],context, True)
	
	context['ue_id']=context['cr_video_camera_url_response']["id"]
	json_response = json.dumps(context['cr_video_camera_url_response'], indent=4)
	MSA_API.task_success(json_response,context, True)
except json.decoder.JSONDecodeError:
	MSA_API.task_error(context['cr_video_camera_url_response'],context, True)