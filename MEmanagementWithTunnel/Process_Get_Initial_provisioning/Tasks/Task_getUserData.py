import json
import base64

from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order

# List all the parameters required by the task
dev_var = Variables()
dev_var.add('userDataBase64', var_type='String')

context = Variables.task_call(dev_var)

device_id = context['vpnConcentratorId']
devicelongid = device_id[3:]

object_parameters = {}
object_parameters['openVpnManagement'] = {}
object_parameters['openVpnManagement'][context['ME_name']] = {}
object_parameters['openVpnManagement'][context['ME_name']]['object_id'] = context['ME_name']

# call the CREATE for the specified MS for each device
order = Order(devicelongid)
order.command_execute('READ', object_parameters)

# convert dict object into json
content = json.loads(order.content)

# check if the response is OK
if order.response.ok:
    userDataHeader='#!/bin/bash\n\
\n\
#Modify SSHD config to allow password authentication for root\n\
sed -i "s/PermitRootLogin.*/PermitRootLogin yes/g" /etc/ssh/sshd_config\n\
sed -i "s/#PermitRootLogin.*/PermitRootLogin yes/g" /etc/ssh/sshd_config\n\
\n\
sed -i "s/PasswordAuthentication.*/PasswordAuthentication yes/g" /etc/ssh/sshd_config\n\
sed -i "s/#PasswordAuthentication.*/PasswordAuthentication yes/g" /etc/ssh/sshd_config\n\
\n\
systemctl restart sshd\n\
\n\
#Create and change user password\n\
useradd '+context['ME_login']+'\n\
echo "'+context['ME_login']+':'+context['ME_password']+'" | sudo chpasswd\n\
\n\
apt install openvpn -y\n\
\n\
echo  \''

    userDataFooter='\'> /etc/openvpn/client.conf\n\
\n\
sudo systemctl enable openvpn@client.service --now\n\
\n\
'

    message = content['message'].replace('!', '\n')
    userdata=userDataHeader+message+userDataFooter
    
    if context['userDataBase64']:
      userData_bytes = userdata.encode("ascii")
      userData_bytes = base64.b64encode(userData_bytes)
      context['userData'] = userData_bytes.decode("ascii")    
    else:
      context['userData']=userdata

    ret = MSA_API.process_content('ENDED',
                                  f'STATUS: {content["status"]}, \
                                    MESSAGE: successfull',
                                  context, True)
                                  
else:
    ret = MSA_API.process_content('FAILED',
                                  f'Import failed \
                                  - {order.content}',
                                  context, True)

print(ret)

