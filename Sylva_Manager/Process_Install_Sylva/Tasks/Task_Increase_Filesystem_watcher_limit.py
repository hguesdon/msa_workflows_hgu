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

p = subprocess.Popen(["ssh -o BatchMode=yes -o ConnectTimeout=10 root@"+ip+" echo ok"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
output = ""
for t in p:
	if re.search("Permission denied",t.decode('utf-8')) != None:
		ret = MSA_API.process_content('FAILED', 'Make sure you have passwordless access. Connection Failed - '+str( t.decode('utf-8')), context, True)
		print(ret)


p = subprocess.Popen(["ssh  root@"+ip+" \"echo fs.inotify.max_user_watches = 524288 |  tee -a /etc/sysctl.conf \" "], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
maxUserWatchesSet = False
for t in p:
	if re.search("max_user_watches",t.decode('utf-8')) != None:
		maxUserWatchesSet = True
if maxUserWatchesSet == False:
	ret = MSA_API.process_content('FAILED', 'Failed setting max_user_watches - '+str( t.decode('utf-8')), context, True)
	print(ret)

p = subprocess.Popen(["ssh  root@"+ip+" \"echo fs.inotify.max_user_instances = 512 |  tee -a /etc/sysctl.conf \" "], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
maxUserInstanceSet = False
for t in p:
	if re.search("max_user_instances",t.decode('utf-8')) != None:
		maxUserInstanceSet = True
if maxUserInstanceSet == False:
	ret = MSA_API.process_content('FAILED', 'Failed setting max_user_instances - '+str( t.decode('utf-8')), context, True)
	print(ret)

p = subprocess.Popen(["ssh  root@"+ip+" sudo sysctl -p /etc/sysctl.conf "], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
for t in p:
	output = output + str( t.decode('utf-8'))+" \r\n"


ret = MSA_API.process_content('ENDED', 'Task OK '+ output, context, True)
print(ret)

