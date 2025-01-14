import json
import uuid
import time
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order

# List all the parameters required by the task
dev_var = Variables()
dev_var.add('BGP_loopback_int_config.0.object_id', var_type='String')
dev_var.add('BGP_loopback_int_config.0.port_name', var_type='String')
dev_var.add('BGP_loopback_int_config.0.ip', var_type='IpAddress')
dev_var.add('BGP_loopback_int_config.0.looptemp_name', var_type='String')

context = Variables.task_call(dev_var)


# read the ID of the selected managed entity
device_id = context['fmg_me']

# extract the database ID
devicelongid = device_id[3:]
order = Order(devicelongid)

context['object_id']='IPSEC'
object_id=context['object_id']

for bgp in context['BGP_loopback_int_config']:
	object_parameters = {}
	object_parameters['Loopback_Int_Config']={}
	object_parameters['Loopback_Int_Config'][object_id]={}
	for key, value in bgp.items():
		object_parameters['Loopback_Int_Config'][object_id][key]={}
		object_parameters['Loopback_Int_Config'][object_id][key]=value
		
	order.command_execute('CREATE', object_parameters)

# convert dict object into json
	content = json.loads(order.content)

order.command_synchronize(300)
MSA_API.task_success('DONE',context, True)