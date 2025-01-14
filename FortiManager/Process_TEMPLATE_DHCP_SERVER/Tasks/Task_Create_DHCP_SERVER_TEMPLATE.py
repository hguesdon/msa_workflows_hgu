import json
import uuid
import time
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order

# List all the parameters required by the task
dev_var = Variables()
dev_var.add('dhcp_server.0.object_id', var_type='String')
dev_var.add('dhcp_server.0.dhcp_server_template_name', var_type='String')
dev_var.add('dhcp_server.0.gateway_ip', var_type='String')
dev_var.add('dhcp_server.0.subnetmask', var_type='String')
dev_var.add('dhcp_server.0.port_name', var_type='String')
dev_var.add('dhcp_server.0.start_ip', var_type='String')
dev_var.add('dhcp_server.0.end_ip', var_type='String')
dev_var.add('dhcp_server.0.fmg_ip', var_type='String')

context = Variables.task_call(dev_var)

# read the ID of the selected managed entity
device_id = context['fmg_me']

# extract the database ID
devicelongid = device_id[3:]
order = Order(devicelongid)

context['object_id']='DHCP_SERVER'
object_id=context['object_id']

for dhcp in context['dhcp_server']:
	object_parameters = {}
	object_parameters['TEMPLATE_DHCP_SERVER']={}
	object_parameters['TEMPLATE_DHCP_SERVER'][object_id]={}
	for key, value in dhcp.items():
		object_parameters['TEMPLATE_DHCP_SERVER'][object_id][key]={}
		object_parameters['TEMPLATE_DHCP_SERVER'][object_id][key]=value
		
	order.command_execute('CREATE', object_parameters)

# convert dict object into json
	content = json.loads(order.content)
order.command_synchronize(300)
MSA_API.task_success('DONE',context, True)