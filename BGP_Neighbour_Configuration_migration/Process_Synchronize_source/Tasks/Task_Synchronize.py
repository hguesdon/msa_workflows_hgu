import json
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order
from msa_sdk import util

# List all the parameters required by the task
dev_var = Variables()
dev_var.add('device_id', var_type='Device')
dev_var.add('dst_device_id', var_type='Device')

context = Variables.task_call(dev_var)

# read the ID of the selected managed entity
device_id = context['device_id']

# extract the database ID
devicelongid = device_id[3:]

# build the Microservice JSON params
#{"Gateway":"0"}
#micro_service_vars_array = {"object_id":object_id}
object_parameters = {}

object_parameters['bgp_neighbour'] = '0';


# call the CREATE for the specified MS for each device
order = Order(devicelongid)
order.command_execute('IMPORT', object_parameters)

# convert dict object into json
content = json.loads(order.content)
process_id = context['SERVICEINSTANCEID']

util.log_to_process_file(process_id, 'naveen:'+content['message'])
result=json.loads(content['message'])['bgp_neighbour']

order.command_objects_instances('bgp_neighbour')
objs= json.loads(order.content)

mylist = []
for item in objs:
    order.command_objects_instances_by_id('bgp_neighbour', item)
    mylist.append(json.loads(order.content)['bgp_neighbour'][item])
context['bgp_neighbour']=mylist;

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

