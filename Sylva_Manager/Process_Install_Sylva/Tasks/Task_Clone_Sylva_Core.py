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

output=""
# p = subprocess.Popen(["ssh  root@"+ip+" \"if test -d /root/sylva-core\; then echo exist\; fi\" "], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
# for t in p:
# 	output = output + str( t.decode('utf-8'))+" \r\n"
# if str(output).strip() == "exist":
# 	p = subprocess.Popen(["ssh  root@"+ip+" rm -rf /root/sylva-core "], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
p = subprocess.Popen(["ssh  root@"+ip+"  git clone https://gitlab.com/sylva-projects/sylva-core.git "], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
for t in p:
	output = output + str( t.decode('utf-8'))+" \r\n"
p = subprocess.Popen(["ssh  root@"+ip+" \"cd /root/sylva-core && git reset --hard 2459dbc8c8cadeb71fc66b25ed19bc88b04853e2 \""], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
for t in p:
	output = output + str( t.decode('utf-8'))+" \r\n"

p = subprocess.Popen(["ssh  root@"+ip+" cp -r /root/sylva-core/environment-values/workload-clusters/kubeadm-capd/ /root/sylva-core/environment-values/workload-clusters/my-kubeadm-capd/   "], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
for t in p:
	output = output + str( t.decode('utf-8'))+" \r\n"



# dockerInstalled = False
# for t in p:
# 	if re.search("Client",t.decode('utf-8')) != None:
# 		dockerInstalled = True
# if dockerInstalled == False:
# 	p = subprocess.Popen(["ssh  root@"+ip+" apt install --assume-yes docker.io "], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
# 	output = ""
	
# else:
# 	output = "Docker already installed"

ret = MSA_API.process_content('ENDED', 'Task OK '+ output, context, True)
print(ret)

