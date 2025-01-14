'''
Visit http://[YOUR_MSA_URL]/msa_sdk/ to see what you can import.
'''
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
import subprocess
import re

dev_var = Variables()
dev_var.add('ip', var_type='IPAddress')
dev_var.add('user', var_type='String')



context = Variables.task_call(dev_var)
ip = str(context['ip']) 
user = str(context['user']) 

p = subprocess.Popen(["ssh "+user+"@"+ip], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
output = ""
# for t in p:
# 	if re.search("Permission denied",t.decode('utf-8')) != None:
# 		ret = MSA_API.process_content('FAILED', 'Make sure you have passwordless access. Connection Failed - '+str( t.decode('utf-8')), context, True)
# 		print(ret)


ret = MSA_API.process_content('ENDED', 'Task OK ', context, True)
print(ret)

