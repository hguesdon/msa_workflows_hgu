'''
Visit http://[YOUR_MSA_URL]/msa_sdk/ to see what you can import.
'''
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
import subprocess
import re

'''
List all the parameters required by the task

You can use var_name convention for your variables
They will display automaticaly as "Var Name"
The allowed types are:
  'String', 'Boolean', 'Integer', 'Password', 'IpAddress',
  'IpMask', 'Ipv6Address', 'Composite', 'OBMFRef', 'Device'

 Add as many variables as needed
'''
dev_var = Variables()


context = Variables.task_call(dev_var)
ip = str(context['ip']) 


p = subprocess.Popen(["ssh  root@"+ip+" docker network inspect kind "], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
output = ""
for t in p:
	output = output + str( t.decode('utf-8'))+" \r\n"

if "not" in output:
	p = subprocess.Popen(["ssh  root@"+ip+" docker network create kind "], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
	p = subprocess.Popen(["ssh  root@"+ip+" docker network inspect kind "], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
	output = ""
	for t in p:
		output = output + str( t.decode('utf-8'))+" \r\n"
	if "not" in output:
		ret = MSA_API.process_content('FAILED', 'Cannot setup kind network'+output, context, True)
		print(ret)
	
ret = MSA_API.process_content('ENDED', 'Task OK '+ output, context, True)
print(ret)

