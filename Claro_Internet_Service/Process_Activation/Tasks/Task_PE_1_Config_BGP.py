import json
import uuid
import time
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order

# List all the parameters required by the task
dev_var = Variables()
dev_var.add('pe_1_bgp.0.bgp_as', var_type='String')
dev_var.add('pe_1_bgp.0.neighbor', var_type='String')
dev_var.add('pe_1_bgp.0.remote_as', var_type='String')
dev_var.add('pe_1_bgp.0.route_map', var_type='String')
context = Variables.task_call(dev_var)

# read the ID of the selected managed entity
device_id = context['device_a']

# extract the database ID
devicelongid = device_id[3:]
order = Order(devicelongid)
for device in context['pe_1_bgp']:
	object_id=device['bgp_as']
	object_parameters = {}
	object_parameters['bgp_internet']={}
	object_parameters['bgp_internet'] [object_id]={}
	object_parameters['bgp_internet'] [object_id]['object_id']=device['bgp_as']
	object_parameters['bgp_internet'] [object_id]['neighbor']=device['neighbor']
	object_parameters['bgp_internet'] [object_id]['remote_as']=device['remote_as']
	object_parameters['bgp_internet'] [object_id]['route_map']=device['route_map']
	order.command_execute('CREATE', object_parameters)


# convert dict object into json
content = json.loads(order.content)

# check if the response is OK
if order.response.ok:
    ret = MSA_API.process_content('ENDED',
                                  f'STATUS: {order.content}, \
                                    MESSAGE: successfull',
                                  context, True)
else:
    ret = MSA_API.process_content('FAILED',
                                  f'Create failed \
                                  - {order.content}',
                                  context, True)

print(ret)

#MSA_API.task_success('DONE',context, True)