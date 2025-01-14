'''
Visit http://[YOUR_MSA_URL]/msa_sdk/ to see what you can import.
'''
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
import subprocess

dev_var = Variables()
context = Variables.task_call(dev_var)
# edgeIp = str(context['edge_ip']) 

p = subprocess.Popen(["ssh root@10.31.1.5   /home/ubuntu/sylva-core/bin/kubectl create ns free5gc "], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
output = ""
for t in p:
	print(t)
	output = output + str(t)

ret = MSA_API.process_content('ENDED', 'Task OK.'+output, context, True)
print(ret)

