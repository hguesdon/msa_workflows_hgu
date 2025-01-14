import json
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order
from msa_sdk import util
# List all the parameters required by the task
dev_var = Variables()
dev_var.add('dst_device_id', var_type='Device')
dev_var.add('vrf.0.iface_raw_string', var_type='String')
dev_var.add('vrf.0.object_id', var_type='String')
dev_var.add('vrf.0.interfaces.0.iface_name', var_type='OBMFRef')
dev_var.add('vrf.0.rd', var_type='String')
dev_var.add('vrf.0.route_target_export', var_type='String')
dev_var.add('vrf.0.route_target_import', var_type='String')

context = Variables.task_call(dev_var)

# read the ID of the selected managed entity
device_id = context['dst_device_id']

# extract the database ID
devicelongid = device_id[3:]

# build the Microservice JSON params
#{"Gateway":"0"}
#micro_service_vars_array = {"object_id":object_id}
object_parameters = {}

object_parameters['vrf'] = {}
for v in context['vrf']:
  object_parameters['vrf'][v['object_id']] = v

process_id = context['SERVICEINSTANCEID']
util.log_to_process_file(process_id, 'naveen:'+json.dumps(object_parameters, indent=4))
# call the CREATE for the specified MS for each device
order = Order(devicelongid)
order.command_execute('CREATE', object_parameters)

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

