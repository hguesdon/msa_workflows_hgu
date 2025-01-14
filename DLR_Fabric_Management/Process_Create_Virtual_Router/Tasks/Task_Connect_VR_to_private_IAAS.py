import json
import uuid
import time
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order

dev_var = Variables()
dev_var.add('device_id', var_type='Device')
dev_var.add('Connection.0.object_id', var_type='String')
dev_var.add('Connection.0.name', var_type='String')
dev_var.add('Connection.0.speed', var_type='String')
dev_var.add('Connection.0.description', var_type='String')
dev_var.add('Connection.0.gateway_type', var_type='String')

context = Variables.task_call(dev_var)
env_ref = context["UBIQUBEID"]

# read the ID of the selected managed entity
device_id = context['device_id']

# extract the database ID
devicelongid = device_id[3:]

# build the Microservice JSON params
#{"Gateway":"0"}
#micro_service_vars_array = {"object_id":object_id}
object_parameters = {}

object_parameters['Connection'] = {}

for v in context['Connection']:
  name=v['name']
  if name == "VR to port":
   v['name']= v['name'] + '_' + context["ENV_NAME"]
   object_parameters['Connection'][v['object_id']] = v
   # call the CREATE for the specified MS for each device
   order = Order(devicelongid)
   order.command_execute('CREATE', object_parameters)
   content = json.loads(order.content)
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
   
MSA_API.task_success('Connect VR to Port',context, True)