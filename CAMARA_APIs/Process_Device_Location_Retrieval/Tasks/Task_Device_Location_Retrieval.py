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


url =  "https://api.orange.com/camara/location-retrieval/orange-lab/v0/retrieve"
headers = {'Authorization':accessToken, 'Cache-Control':'no-cache', 'content-type': 'application/json', 'accept':'application/json'}
msisdn = str(context['msisdn']) 

payload = {"device": {"phoneNumber": msisdn}, "maxAge": 60}
r = requests.post(url, data=json.dumps(payload), headers=headers)
message = "Error"
if int(r.status_code) == 200:
    res = r.json()
    if 'area' in res and res['area'] != None:
        message = ("The mobile equipment {} is within the {} with radius={} m and "
          "with center coordinates=({}, {})".format( msisdn, res['area']['areaType'], res['area']['radius'], res['area']['center']['latitude'], res['area']['center']['longitude']))
    else:
        message = ("The mobile %s is not in this zone.", msisdn)
    ret = MSA_API.process_content('ENDED', ''+message+ str(json.dumps(r.json())), context, True)

elif int(r.status_code) == 400:
    message = ("Invalid input provided")
    ret = MSA_API.process_content('FAILED', ''+message+ str(json.dumps(r.json())), context, True)

elif int(r.status_code) == 404:
    message = ("the network is not able to localize the equipment %s",msisdn)
    ret = MSA_API.process_content('FAILED', ''+message+ str(json.dumps(r.json())), context, True)

elif int(r.status_code) == 503:
    message = ("The localisation service is not live")
    ret = MSA_API.process_content('FAILED', ''+message+ str(json.dumps(r.json())), context, True)

print(ret)

