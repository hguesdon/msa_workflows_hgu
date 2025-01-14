import json
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order

# List all the parameters required by the task
dev_var = Variables()

context = Variables.task_call(dev_var)

device_id = context['vpnConcentratorId']
devicelongid = device_id[3:]

object_parameters = {}
object_parameters['openVpnManagement'] = {}
object_parameters['openVpnManagement'][context['ME_name']] = {}
object_parameters['openVpnManagement'][context['ME_name']]['object_id'] = context['ME_name']


# call the CREATE 
order = Order(devicelongid)
order.command_execute('IMPORT', object_parameters)

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

