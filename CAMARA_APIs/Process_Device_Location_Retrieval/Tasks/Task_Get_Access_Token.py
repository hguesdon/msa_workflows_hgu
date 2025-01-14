'''
Visit http://[YOUR_MSA_URL]/msa_sdk/ to see what you can import.
'''
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
import requests

dev_var = Variables()
dev_var.add('provider_app_id', var_type='String')
context = Variables.task_call(dev_var)

url=context['authurl']

if context['apivendor'] == 'Orange':
	#url =  "https://api.orange.com/oauth/v3/token"
	headers = {'Authorization':str(context['authheader']), 'content-type': 'application/x-www-form-urlencoded'}
	payload = "grant_type=client_credentials"

if context['apivendor'] == 'ATT':
	#-d 'client_id=00001111-aaaa-2222-bbbb-3333cccc4444&scope=https%3A%2F%2Fgraph.microsoft.com%2F.default&client_secret=A1bC2dE3f...&grant_type=client_credentials'
	headers = {'content-type': 'application/x-www-form-urlencoded'}
	url = url.replace("{tenant}", context['tenantid'])
	payload = {
		'client_id': context['clientid'],
		'scope': 'api://'+context['provider_app_id']+'/.default',
		'client_secret': context['clientsecret'],
		'grant_type': 'client_credentials'
	}


r = requests.post(url, data=payload, headers=headers)

if r.status_code == 200:
	context['access_token'] = r.json()['access_token']
	ret = MSA_API.process_content('ENDED', 'Task OK', context, True)
else:
	ret = MSA_API.process_content('FAILED', 'Failed to get access token', context, True)
print(ret)

