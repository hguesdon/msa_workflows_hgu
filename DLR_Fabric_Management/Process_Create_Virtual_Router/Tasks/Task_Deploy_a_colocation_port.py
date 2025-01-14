import json
import uuid
import time
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order

dev_var = Variables()
dev_var.add('device_id', var_type='Device')

context = Variables.task_call(dev_var)

# read the ID of the selected managed entity
device_id = context['device_id']

# extract the database ID
devicelongid = device_id[3:]

order = Order(devicelongid)

order.command_synchronize(300)	

MSA_API.task_success('Deploy colocation port OK',context, True)