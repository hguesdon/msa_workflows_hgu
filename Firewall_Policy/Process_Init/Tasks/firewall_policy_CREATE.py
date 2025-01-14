import json
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order

# List all the parameters required by the task
dev_var = Variables()
dev_var.add('device_id', var_type='Device')
dev_var.add('firewall_policy.0.object_id', var_type='AutoIncrement')
dev_var.add('firewall_policy.0.name', var_type='String')
dev_var.add('firewall_policy.0.move_selector', var_type='String')
dev_var.add('firewall_policy.0.move_index', var_type='String')
dev_var.add('firewall_policy.0.status', var_type='Boolean')
dev_var.add('firewall_policy.0.srcintf', var_type='String')
dev_var.add('firewall_policy.0.srcaddr', var_type='String')
dev_var.add('firewall_policy.0.dstintf', var_type='String')
dev_var.add('firewall_policy.0.dstaddr_selector', var_type='String')
dev_var.add('firewall_policy.0.dstaddr', var_type='String')
dev_var.add('firewall_policy.0.dst_nat', var_type='String')
dev_var.add('firewall_policy.0.service', var_type='String')
dev_var.add('firewall_policy.0.action', var_type='String')
dev_var.add('firewall_policy.0.nat', var_type='String')
dev_var.add('firewall_policy.0.naptSelector', var_type='String')
dev_var.add('firewall_policy.0.napt_object', var_type='String')
dev_var.add('firewall_policy.0.logtraffic', var_type='String')
dev_var.add('firewall_policy.0.comments', var_type='String')
dev_var.add('firewall_policy.0.natVerify', var_type='String')
dev_var.add('firewall_policy.0.statusVerify', var_type='String')
dev_var.add('firewall_policy.0.ippoolVerify', var_type='String')
dev_var.add('firewall_policy.0._order', var_type='String')
dev_var.add('firewall_policy.0._prev', var_type='String')
dev_var.add('firewall_policy.0._next', var_type='String')

context = Variables.task_call(dev_var)

# read the ID of the selected managed entity
device_id = context['device_id']

# extract the database ID
devicelongid = device_id[3:]

# build the Microservice JSON params
#{"Gateway":"0"}
#micro_service_vars_array = {"object_id":object_id}
object_parameters = {}

object_parameters['firewall_policy'] = {}
for v in context['firewall_policy']:
  object_parameters['firewall_policy'][v['object_id']] = v


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

