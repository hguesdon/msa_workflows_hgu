'''
Visit http://[YOUR_MSA_URL]/msa_sdk/ to see what you can import.
'''
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
import requests
import json

dev_var = Variables()
dev_var.add('msisdn', var_type='String')


context = Variables.task_call(dev_var)
accessToken = "Bearer "+str(context['access_token']) 


url =  "https://api.orange.com/camara/device-status/orange-lab/v0/status"
headers = {'Authorization':accessToken, 'Cache-Control':'no-cache', 'content-type': 'application/json', 'accept':'application/json'}
msisdn = str(context['msisdn']) 


payload = {"ueId": {"msisdn": msisdn},"eventType": "UE_ROAMING_STATUS"}

r = requests.post(url, data=json.dumps(payload), headers=headers)
message = "Error"
if int(r.status_code) == 200:
    res = r.json()
    ret = MSA_API.process_content('ENDED', 'Success - ' +str(res['eventStatus']) + str(json.dumps(r.json())), context, True)

elif int(r.status_code) == 400:
    message = "Invalid input provided"
    ret = MSA_API.process_content('FAILED', ''+message+ str(json.dumps(r.json())), context, True)

elif int(r.status_code) == 404:
    message = "The network is not able to localize the equipment {}".format(msisdn)
    ret = MSA_API.process_content('FAILED', ''+message+ str(json.dumps(r.json())), context, True)

elif int(r.status_code) == 503:
    message = "The Device status service is not live"
    ret = MSA_API.process_content('FAILED', ''+message+ str(json.dumps(r.json())), context, True)
else:
	ret = MSA_API.process_content('FAILED', 'Operation failed. Check input.'+ str(json.dumps(r.json())), context, True)

print(ret)

