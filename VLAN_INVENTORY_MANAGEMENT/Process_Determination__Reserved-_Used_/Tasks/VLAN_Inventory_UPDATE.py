import json
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order

# List all the parameters required by the task
dev_var = Variables()
dev_var.add('Location_name', var_type='String')
dev_var.add('VLAN_ID', var_type='String')
context = Variables.task_call(dev_var)

# read the ID of the selected managed entity
device_id = context['device_id']

# extract the database ID
devicelongid = device_id[3:]

# build the Microservice JSON params for the order
micro_service_vars_array = {"object_id": 1,
                           "location": context['Location_name'],
                           "vlan_id": context['VLAN_ID'],
                           "segment": "Segment_A",
                           "location_id": "01",
                           "use": "Used"
                           }
object_id = 1

object_parameters = {"VLAN_Inventory": {object_id: micro_service_vars_array}}

# call the CREATE for the specified MS for each device
order = Order(devicelongid)
order.command_execute('UPDATE', object_parameters)

# convert dict object into json
content = json.loads(order.content)

# check if the response is OK
if order.response.ok:
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

