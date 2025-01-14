import json
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order

# List all the parameters required by the task
dev_var = Variables()
dev_var.add('Degree1', var_type='Device')
dev_var.add('OpenRoadm_Interfaces.0.object_id', var_type='String')
dev_var.add('OpenRoadm_Interfaces.0.state', var_type='String')
dev_var.add('OpenRoadm_Interfaces.0.circuit_pack_name', var_type='String')
dev_var.add('OpenRoadm_Interfaces.0.supporting_port', var_type='String')
dev_var.add('OpenRoadm_Interfaces.0.freq', var_type='String')
dev_var.add('OpenRoadm_Interfaces.0.width', var_type='String')

context = Variables.task_call(dev_var)

# read the ID of the selected managed entity
device_id = context['Degree1']

# extract the database ID
devicelongid = device_id[3:]

# build the Microservice JSON params
#{"Gateway":"0"}
#micro_service_vars_array = {"object_id":object_id}
object_parameters = {}

object_parameters['OpenRoadm_Interfaces'] = {}
for v in context['OpenRoadm_Interfaces']:
  object_parameters['OpenRoadm_Interfaces'][v['object_id']] = v


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

