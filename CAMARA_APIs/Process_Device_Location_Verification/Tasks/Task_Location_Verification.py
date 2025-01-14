'''
Visit http://[YOUR_MSA_URL]/msa_sdk/ to see what you can import.
'''
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
import requests
import json

dev_var = Variables()
dev_var.add('msisdn', var_type='String')
dev_var.add('lon', var_type='Integer')
dev_var.add('lat', var_type='Integer')
dev_var.add('accuracy', var_type='Integer')

context = Variables.task_call(dev_var)
accessToken = "Bearer "+str(context['access_token']) 


url =  "https://api.orange.com/camara/location-verification/orange-lab/v0/verify"
headers = {'Authorization':accessToken, 'Cache-Control':'no-cache', 'content-type': 'application/json', 'accept':'application/json'}
msisdn = str(context['msisdn']) 

lat = float(context['lat'])
lon = float(context['lon'])
accuracy = int(context['accuracy'])
payload = {"ueId": {"msisdn": msisdn},"latitude": lat,"longitude" : lon,"accuracy" : accuracy,"maxLocationAge": 100 }

r = requests.post(url, data=json.dumps(payload), headers=headers)
message = "Error"
if int(r.status_code) == 200:
    res = r.json()
    if res['verificationResult'] == True:
        message = "The mobile equipment {} is within the circle with radius={} km and circle with center coordinates=({}, {})".format( msisdn, accuracy, lat, lon)
    else:
        message = "The mobile "+msisdn+" is not in this zone." 
    ret = MSA_API.process_content('ENDED', 'Success - '+message+ str(json.dumps(r.json())), context, True)

elif int(r.status_code) == 400:
    message = "Invalid input provided"
    ret = MSA_API.process_content('FAILED', ''+message+ str(json.dumps(r.json())), context, True)

elif int(r.status_code) == 404:
    message = "The network is not able to localize the equipment {}".format(msisdn)
    ret = MSA_API.process_content('FAILED', ''+message+ str(json.dumps(r.json())), context, True)

elif int(r.status_code) == 503 or int(r.status_code) == 500:
    message = "The localisation service is not live"
    ret = MSA_API.process_content('FAILED', ''+message+ str(json.dumps(r.json())), context, True)
else:
	ret = MSA_API.process_content('FAILED', 'Operation failed. Check input.'+ str(json.dumps(r.json())), context, True)

print(ret)

