import json
import uuid
import time
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order

# List all the parameters required by the task
dev_var = Variables()
dev_var.add('Policy_Map_Internet', var_type='String')
dev_var.add('Prefix_List_Internet', var_type='String')
dev_var.add('bgp_internet', var_type='String')
dev_var.add('Route_Map_Internet', var_type='String')
context = Variables.task_call(dev_var)

# read the ID of the selected managed entity
device_id = context['device_a']
# extract the database ID
devicelongid = device_id[3:]
order = Order(devicelongid)

order.command_synchronize(300)	
MSA_API.task_success('SYNCHRONIZATION DONE',context, True)