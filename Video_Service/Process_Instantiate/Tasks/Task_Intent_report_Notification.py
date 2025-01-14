import re
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.device import Device
from msa_sdk.order import Order
import requests
import urllib3
import time
import json
from datetime import datetime,timedelta
import pytz

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

dev_var = Variables()
dev_var.add('ServiceID', var_type='String')
dev_var.add('description', var_type='String')
dev_var.add('priority', var_type='String')
dev_var.add('SwInfo', var_type='String')
dev_var.add('availability', var_type='String')
dev_var.add('DL_latency', var_type='String')
dev_var.add('DL_ThptPerUE', var_type='String')
dev_var.add('maxNumberOfUEs', var_type='String')
dev_var.add('UserStorageVolume', var_type='String')
dev_var.add('billingAccount', var_type='String')
dev_var.add('externalId', var_type='String')
dev_var.add('serviceOrderId', var_type='String')
context = Variables.task_call(dev_var)


## Getting access_token


url = "https://eu01.sb.infonova.com/auth/realms/SB_NTT_BUSINESSPLACE/protocol/openid-connect/token"
 
payload = "-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"grant_type\"\r\n\r\nclient_credentials\r\n-----011000010111000001101001--\r\n"
headers = {
    "Accept": "application/x-www-form-urlencoded, application/json",
    "Content-Type": "multipart/form-data; boundary=---011000010111000001101001",
    "Authorization": "Basic TVNhY3RpdmF0b3I6OFJ5V3E2ZHFaOE5ROG45dnFKY2Vjams5M0NIUVN0a1Y="
}
 
response = requests.request("POST", url, data=payload, headers=headers)
 
#print(response.text)

r_json = response.json()
context['infonova_access_token']=r_json.get('access_token')



##Sent notification
auth='Bearer ' +context['infonova_access_token']+''
_headers2 = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization':''+auth+'',
}


data2 = {
    'taskDefinition': 'INTENT_REPORT',
    'billingAccount': ''+context['billingAccount']+'',
    'category':'Provisioning',
    'state':'Acknowledged',
    'priority': 1,
    'parameters': {
    	'taskMsg': 'Comming soon: Detailed Intent report',
    	'serviceId': ''+context['externalId']+'',
    }
}

context['data2']=data2

infonova_url = "https://eu01.sb.infonova.com/r6-api/ANHYPER/tasks/v2/tasks/"

context['infonova_url'] = infonova_url

response2 = requests.request("POST", url=infonova_url, headers=_headers2, data=json.dumps(data2), verify=False)
r_json2 = response2.json()
context.update(infonova_response = dict(response=r_json2,satus_code=response2.status_code))

MSA_API.task_success('Infonova Order state Change Notification for order sent\n Status Code : '+str(response2.status_code)+'', context, True)
