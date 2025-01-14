import json
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order
from msa_sdk.customer import Customer

# List all the parameters required by the task
dev_var = Variables()
dev_var.add('device_id', var_type='Device')
dev_var.add('port', var_type='OBMFRef')
dev_var.add('Virtual_Router.0.object_id', var_type='String')
dev_var.add('Virtual_Router.0.asn', var_type='String')
dev_var.add('Virtual_Router.0.description', var_type='String')
dev_var.add('Virtual_Router.0.name', var_type='String')
dev_var.add('Virtual_Router.0.operational_state', var_type='String')
dev_var.add('Virtual_Router.0.speed', var_type='String')
dev_var.add('Virtual_Router.0.location', var_type='String')

context = Variables.task_call(dev_var)
env_ref = context["UBIQUBEID"]

# read the ID of the selected managed entity
device_id = context['device_id']

# extract the database ID
devicelongid = device_id[3:]
customerId = env_ref[4:]

env = Customer()
retEnv = json.loads(env.get_customer_by_id(customerId))
context["ENV_NAME"] = retEnv['name']

# build the Microservice JSON params
#{"Gateway":"0"}
#micro_service_vars_array = {"object_id":object_id}
object_parameters = {}

object_parameters['Virtual_Router'] = {}

for v in context['Virtual_Router']:
  name=v['name']
  if name == "CCLA_RANDOM":
    v['name']= context["ENV_NAME"]
  object_parameters['Virtual_Router'][v['object_id']] = v

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

