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
dev_var.add('MEC_node', var_type='Device')
dev_var.add('externalId', var_type='String')
dev_var.add('relatedParties.0.role', var_type='String')
dev_var.add('relatedParties.0.id', var_type='String')
dev_var.add('relatedParties.0.name', var_type='String')
context = Variables.task_call(dev_var)

tab = context['relatedParties']
found_value=''

for item in tab:
 if item.get('role') and item['role'] == 'SERVICE_PROVIDER':
   found_value= item['id']
 
context['found_value'] = found_value

## Getting access_token

headers = {
    'Accept': 'application/json',
}

data = {
    'client_id': 'tm-nodered',
    'client_secret': 'AzKvAsmdxe',
    'grant_type': 'password',
    'username': 'admin_aws_us',
    'password': 'Demo123!',
}

_headers = {'Accept': 'application/json'}
        
response = requests.request("POST", url='https://eu01.sb.infonova.com/auth/realms/SB_CATALYST/protocol/openid-connect/token', headers=_headers, data=data, verify=False)
r_json = response.json()
context['infonova_access_token']=r_json.get('access_token')


##Sent notification
auth='Bearer ' +context['infonova_access_token']+''
_headers2 = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization':''+auth+'',
}

now = datetime.now(pytz.timezone("Europe/Paris"))
date_time = now.strftime("%Y-%m-%dT%H:%M:%S%z")

date_time_str = "{0}:{1}".format(
  date_time[:-2],
  date_time[-2:]
)

next_date_time=datetime.strptime(date_time,"%Y-%m-%dT%H:%M:%S%z")
next_date_time=next_date_time  + timedelta(days=1)
next_date_time=next_date_time.strftime("%Y-%m-%dT%H:%M:%S%z")
next_date_time_str = "{0}:{1}".format(
  next_date_time[:-2],
  next_date_time[-2:]
)

data2 = {
    'id': ''+context['externalId']+'',
    'dateTime': ''+date_time_str+'',
    'eventType': 'orderStateChangeNotification',
    'serviceOrder': {
    'id': ''+context['externalId']+'',
    'externalId': ''+context['externalId']+'',
    'state':'Completed',
    'priority': 4,
    'expectedCompletionDate': ''+next_date_time_str+''
    }
}

context['data2']=data2

infonova_url = "https://eu01.sb.infonova.com/r6-api/"+found_value+"/serviceordering/v1/notification"

context['infonova_url'] = infonova_url

response2 = requests.request("POST", url=infonova_url, headers=_headers2, data=json.dumps(data2), verify=False)
r_json2 = response2.json()
context.update(infonova = dict(response=r_json2,satus_code=response2.status_code))

MSA_API.task_success('Infonova Order state Change Notification for order sent\n Status Code : '+str(response2.status_code)+'', context, True)
