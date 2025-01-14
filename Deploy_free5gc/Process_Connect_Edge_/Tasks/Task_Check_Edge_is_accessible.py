
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
import subprocess


dev_var = Variables()
dev_var.add('cluster')


context = Variables.task_call(dev_var)
context['cluster'] = str(context['cluster']) 

# p = subprocess.Popen(["ssh ubuntu@10.31.1.5 touch /home/ubuntu/44.txt"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
# output = ""
# for t in p:
	# print(t)
	# output = output + str(t)
ret = MSA_API.process_content('ENDED', 'Task OK', context, True)
print(ret)

