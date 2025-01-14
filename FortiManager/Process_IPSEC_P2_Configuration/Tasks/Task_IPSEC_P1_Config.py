import json
import uuid
import time
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order

# List all the parameters required by the task
dev_var = Variables()

dev_var.add('IPSEC_p2_config.0.object_id', var_type='String')
dev_var.add('IPSEC_p2_config.0.tunnel_p2_name1', var_type='String')
dev_var.add('IPSEC_p2_config.0.tunnel_p1_name1', var_type='String')
dev_var.add('IPSEC_p2_config.0.proposal_name1', var_type='String')
dev_var.add('IPSEC_p2_config.0.tunnel_p2_name2', var_type='String')
dev_var.add('IPSEC_p2_config.0.tunnel_p1_name2', var_type='String')
dev_var.add('IPSEC_p2_config.0.proposal_name2', var_type='String')
dev_var.add('IPSEC_p2_config.0.keylifeseconds', var_type='String')
dev_var.add('IPSEC_p2_config.0.tunnel_p2_name3', var_type='String')
dev_var.add('IPSEC_p2_config.0.tunnel_p1_name3', var_type='String')
dev_var.add('IPSEC_p2_config.0.keylifekbs', var_type='String')
dev_var.add('IPSEC_p2_config.0.tunnel_p2_name4', var_type='String')
dev_var.add('IPSEC_p2_config.0.tunnel_p1_name4', var_type='String')
dev_var.add('IPSEC_p2_config.0.IPSEC_p2_template_name', var_type='String')
context = Variables.task_call(dev_var)

# read the ID of the selected managed entity
device_id = context['fmg_me']

# extract the database ID
devicelongid = device_id[3:]
order = Order(devicelongid)
'''
object_id=device['name']
object_parameters = {}
object_parameters['FortiManager_-_Devices']={}
object_parameters['FortiManager_-_Devices'] [object_id]={}
object_parameters['FortiManager_-_Devices'] [object_id]['object_id']=device['name']
object_parameters['FortiManager_-_Devices'] [object_id]['user_name']=device['username']
object_parameters['FortiManager_-_Devices'] [object_id]['user_password']=device['password']
object_parameters['FortiManager_-_Devices'] [object_id]['ip_address']=device['ip']
order.command_execute('CREATE', object_parameters)

# convert dict object into json
	content = json.loads(order.content)

'''
MSA_API.task_success('DONE',context, True)