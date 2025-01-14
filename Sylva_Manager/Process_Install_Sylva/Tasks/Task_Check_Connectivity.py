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
dev_var.add('ip', var_type='IpAddress')

context = Variables.task_call(dev_var)
ip = str(context['ip']) 

p = subprocess.Popen(["ssh -o BatchMode=yes -o ConnectTimeout=10 root@"+ip+" echo ok"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
output = ""
for t in p:
	output = output + str(t.decode('utf-8'))
	# if re.search("Permission denied",t.decode('utf-8')) != None:
	# 	ret = MSA_API.process_content('FAILED', 'Make sure you have passwordless access. Connection Failed - '+str( t.decode('utf-8')), context, True)
	# 	print(ret)

if str(output).strip() != "ok":
	ret = MSA_API.process_content('FAILED', 'Connection Failed '+output, context, True)
	print(ret)
ret = MSA_API.process_content('ENDED', 'Connection success - '+output, context, True)
print(ret)

