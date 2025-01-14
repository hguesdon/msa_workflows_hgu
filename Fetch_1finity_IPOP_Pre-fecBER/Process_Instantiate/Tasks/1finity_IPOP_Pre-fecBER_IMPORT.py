import json
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order

# List all the parameters required by the task
dev_var = Variables()
dev_var.add('device_id', var_type='Device')
dev_var.add('FECbitErrorRate', var_type='String')
dev_var.add('Timestamp', var_type='String')
dev_var.add('Entity', var_type='String')
dev_var.add('Port', var_type='String')

context = Variables.task_call(dev_var)

# read the ID of the selected managed entity
device_id = context['device_id']

# extract the database ID
devicelongid = device_id[3:]

# build the Microservice JSON params
#{"Gateway":"0"}
#micro_service_vars_array = {"object_id":object_id}
object_parameters = {}

object_parameters['1finity_IPOP_Pre-fecBER'] = '0';


# call the CREATE for the specified MS for each device
order = Order(devicelongid)
order.command_execute('IMPORT', object_parameters)

# convert dict object into json
content = json.loads(order.content)
context.update(content = content)

# Extracting the 'message' field which is a JSON string
message = content['message']

# Parsing the JSON string inside the 'message' field
message_dict = json.loads(message)

# Navigating through the dictionary to extract FECbitErrorRate and timestamp
fecbit_error_rate = message_dict['1finity_IPOP_Pre-fecBER']['FECbitErrorRate']['pm_value'].strip()
timestamp = message_dict['1finity_IPOP_Pre-fecBER']['FECbitErrorRate']['timestamp'].replace(' ', 'T')

# Saving the extracted values
context['FECbitErrorRate'] = fecbit_error_rate
context['Timestamp'] = timestamp

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

