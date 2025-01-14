import json
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order

# List all the parameters required by the task
dev_var = Variables()
dev_var.add('device_id', var_type='Device')
dev_var.add('instances.0.object_id', var_type='AutoIncrement')
dev_var.add('instances.0.name', var_type='String')
dev_var.add('instances.0.instance_id', var_type='String')
dev_var.add('instances.0.image_id', var_type='String')
dev_var.add('instances.0.security_groups', var_type='OBMFRef')
dev_var.add('instances.0.subnet_id', var_type='OBMFRef')
dev_var.add('instances.0.vpc_id', var_type='OBMFRef')
dev_var.add('instances.0.private_ip_address', var_type='String')
dev_var.add('instances.0.public_dns_name', var_type='String')
dev_var.add('instances.0.Placement.0.availability_zone', var_type='String')
dev_var.add('instances.0.Placement.0.group_name', var_type='String')
dev_var.add('instances.0.Placement.0.tenancy', var_type='String')
dev_var.add('instances.0.availability_zone', var_type='OBMFRef')
dev_var.add('instances.0.instance_type', var_type='String')
dev_var.add('instances.0.max_count', var_type='Integer')
dev_var.add('instances.0.min_count', var_type='Integer')
dev_var.add('instances.0.state_name', var_type='String')
dev_var.add('instances.0.dns_name', var_type='String')
dev_var.add('instances.0.State.0.state_name', var_type='String')
dev_var.add('instances.0.tags.0.tag_key', var_type='String')
dev_var.add('instances.0.tags.0.tag_value', var_type='String')
dev_var.add('instances.0.state_transition_reason', var_type='String')
dev_var.add('instances.0.SecurityGroups.0.group_id', var_type='String')
dev_var.add('instances.0.SecurityGroups.0.group_name', var_type='String')
dev_var.add('instances.0.hypervisor', var_type='String')
dev_var.add('instances.0.launch_time', var_type='String')
dev_var.add('instances.0.virtualization_type', var_type='String')
dev_var.add('instances.0._color', var_type='String')

context = Variables.task_call(dev_var)

# read the ID of the selected managed entity
device_id = context['device_id']

# extract the database ID
devicelongid = device_id[3:]

# build the Microservice JSON params
#{"Gateway":"0"}
#micro_service_vars_array = {"object_id":object_id}
object_parameters = {}

object_parameters['instances'] = {}
for v in context['instances']:
  object_parameters['instances'][v['object_id']] = v


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

