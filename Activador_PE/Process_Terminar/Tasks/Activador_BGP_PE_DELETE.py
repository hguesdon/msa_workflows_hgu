import json
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order

# List all the parameters required by the task
dev_var = Variables()
dev_var.add('device_id', var_type='Device')
dev_var.add('Activador_BGP_PE.0.object_id', var_type='String')
dev_var.add('Activador_BGP_PE.0.name', var_type='String')
dev_var.add('Activador_BGP_PE.0.asn', var_type='String')
dev_var.add('Activador_BGP_PE.0.password', var_type='Password')
dev_var.add('Activador_BGP_PE.0.description', var_type='String')
dev_var.add('Activador_BGP_PE.0.cid', var_type='String')
dev_var.add('Activador_BGP_PE.0.LAN', var_type='IpAddress')
dev_var.add('Activador_BGP_PE.0.mask', var_type='Integer')
dev_var.add('Activador_BGP_PE.0.ipwancpe', var_type='IpAddress')

context = Variables.task_call(dev_var)

# read the ID of the selected managed entity
device_id = context['device_id']

# extract the database ID
devicelongid = device_id[3:]

# build the Microservice JSON params
#{"Gateway":"0"}
#micro_service_vars_array = {"object_id":object_id}
object_parameters = {}

object_parameters['Activador_BGP_PE'] = {}
for v in context['Activador_BGP_PE']:
  object_parameters['Activador_BGP_PE'][v['object_id']] = v


# call the CREATE for the specified MS for each device
order = Order(devicelongid)
order.command_execute('DELETE', object_parameters)

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

