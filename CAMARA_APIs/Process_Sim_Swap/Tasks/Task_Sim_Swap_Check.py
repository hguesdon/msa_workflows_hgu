'''
Visit http://[YOUR_MSA_URL]/msa_sdk/ to see what you can import.
'''
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
import requests
import json

dev_var = Variables()
dev_var.add('msisdn', var_type='String')
dev_var.add('maxage', var_type='Integer')

context = Variables.task_call(dev_var)

msisdn = str(context['msisdn']) 

if context['apivendor'] == 'Orange':
	accessToken = "Bearer "+str(context['access_token']) 
	url =  "https://api.orange.com/camara/sim-swap/ofr/v0/check"
	headers = {'Authorization':accessToken, 'Cache-Control':'no-cache', 'content-type': 'application/json', 'accept':'application/json'}
	payload = {"phoneNumber": msisdn,"maxAge": int(context['maxage'])}

if context['apivendor'] == 'ATT':
	access_token = context['access_token']
	url = "https://x-camara-ss.nprd-gw.cloud.att.com/sim-swap/v0/check"
	headers = {
		"Content-Type": "application/json",
		"Authorization": f"Bearer {access_token}",
		"User-Agent": "MyApp/1.0" 
	}
	payload = {
		"phoneNumber": msisdn,
		"maxAge": int(context['maxage'])
	}


r = requests.post(url, data=json.dumps(payload), headers=headers)
message = "Error"
if int(r.status_code) == 200:
    res = r.json()
    if res['swapped'] == True:
        message = "A sim swap has been done for {} ".format( msisdn)
        context['swap'] = 1
    else:
        message = "No sim swap happened for {} ".format( msisdn)
        context['swap'] = 0
    
    ret = MSA_API.process_content('ENDED', '' +message+ str(json.dumps(r.json())), context, True)

elif int(r.status_code) == 400:
    message = "Invalid input provided"
    ret = MSA_API.process_content('FAILED', ''+message+ str(json.dumps(r.json())), context, True)

elif int(r.status_code) == 404:
    message = "The network is not able to localize the equipment {}".format(msisdn)
    ret = MSA_API.process_content('FAILED', ''+message+ str(json.dumps(r.json())), context, True)

elif int(r.status_code) == 503:
    message = "The Device status service is not live"
    ret = MSA_API.process_content('FAILED', ''+message+ str(json.dumps(r.json())), context, True)

elif int(r.status_code) == 403:
    message = "Error 403: Forbidden - Possible issues with access token or permissions."
    ret = MSA_API.process_content('FAILED', ''+message+ str(json.dumps(r.json())), context, True)

else:
	ret = MSA_API.process_content('FAILED', 'Operation failed. Check input.'+ str(json.dumps(r.json())), context, True)

print(ret)

