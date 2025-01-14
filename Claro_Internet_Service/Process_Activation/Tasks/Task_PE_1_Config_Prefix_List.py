import json
import uuid
import time
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order

# List all the parameters required by the task
dev_var = Variables()
dev_var.add('pe_1_prefix_list.0.list_name', var_type='String')
dev_var.add('pe_1_prefix_list.0.action', var_type='String')
dev_var.add('pe_1_prefix_list.0.address', var_type='String')
context = Variables.task_call(dev_var)

# read the ID of the selected managed entity
device_id = context['device_a']

# extract the database ID
devicelongid = device_id[3:]
order = Order(devicelongid)
for device in context['pe_1_prefix_list']:
	object_id=device['list_name']
	object_parameters = {}
	object_parameters['Prefix_List_Internet']={}
	object_parameters['Prefix_List_Internet'] [object_id]={}
	object_parameters['Prefix_List_Internet'] [object_id]['object_id']=device['list_name']
	object_parameters['Prefix_List_Internet'] [object_id]['action']=device['action']
	object_parameters['Prefix_List_Internet'] [object_id]['address']=device['address']
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