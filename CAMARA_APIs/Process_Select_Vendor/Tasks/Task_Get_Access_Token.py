
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
import requests

dev_var = Variables()
dev_var.add('apivendor', var_type='String')
dev_var.add('tenantid', var_type='String')
dev_var.add('authurl', var_type='String')
dev_var.add('clientid', var_type='String')
dev_var.add('clientsecret', var_type='Password')
dev_var.add('authheader', var_type='String')
context = Variables.task_call(dev_var)

context['apivendor'] = str(context['apivendor']) 
context['authheader'] = str(context['authheader']) 



ret = MSA_API.process_content('ENDED', 'Task OK ', context, True)
print(ret)

