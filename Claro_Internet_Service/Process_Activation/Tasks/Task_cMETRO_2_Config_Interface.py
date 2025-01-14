import json
import uuid
import time
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order

# List all the parameters required by the task
dev_var = Variables()
dev_var.add('cMETRO_2_interface.0.name', var_type='String')
dev_var.add('cMETRO_2_interface.0.description', var_type='String')
dev_var.add('cMETRO_2_interface.0.mode', var_type='String')
dev_var.add('cMETRO_2_interface.0.vlan', var_type='String')
dev_var.add('cMETRO_2_interface.0.policy_map_in', var_type='String')
dev_var.add('cMETRO_2_interface.0.policy_map_out', var_type='String')
context = Variables.task_call(dev_var)

# read the ID of the selected managed entity
device_id = context['device_d']

# extract the database ID
devicelongid = device_id[3:]
order = Order(devicelongid)
for device in context['cMETRO_2_interface']:
	object_id=device['name']
	object_parameters = {}
	object_parameters['Interface_Internet']={}
	object_parameters['Interface_Internet'] [object_id]={}
	object_parameters['Interface_Internet'] [object_id]['object_id']=device['name']
	object_parameters['Interface_Internet'] [object_id]['description']=device['description']
	object_parameters['Interface_Internet'] [object_id]['mode']=device['mode']
	object_parameters['Interface_Internet'] [object_id]['vlan']=device['vlan']
	object_parameters['Interface_Internet'] [object_id]['policy_map_in']=device['policy_map_in']
	object_parameters['Interface_Internet'] [object_id]['policy_map_out']=device['policy_map_out']
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