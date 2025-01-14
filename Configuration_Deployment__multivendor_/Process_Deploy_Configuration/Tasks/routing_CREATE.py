import json
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order
from msa_sdk import util
from msa_sdk.orchestration import Orchestration


# List all the parameters required by the task
dev_var = Variables()
dev_var.add('subnet')
dev_var.add('mask')
dev_var.add('gateway')
dev_var.add('vlan_name')
dev_var.add('vlan_id')
context = Variables.task_call(dev_var)

process_id = context['SERVICEINSTANCEID']
Orchestration = Orchestration(context['UBIQUBEID'])
async_update_list = (context['PROCESSINSTANCEID'], context['TASKID'], context['EXECNUMBER'])
Orchestration.update_asynchronous_task_details(*async_update_list, 'Configuration update started')

devices = context['devices']
for device in devices:
  # extract the database ID
  device_db_id = device['id'][3:]
  Orchestration.update_asynchronous_task_details(*async_update_list, 'Updating device: '+device['id']+'')

  # build the Microservice JSON params for the CREATE
  micro_service_vars_array = {"object_id": context['vlan_id'],                       
                              "mask": context['mask'],
                              "subnet": context['subnet'],
                              "gateway": context['gateway'],
                              "vlan_name": context['vlan_name'],
                              "vlan_id": context['vlan_id']
                              }
                              
  object_id = context['vlan_id']
  config = {"initial_config": {object_id: micro_service_vars_array}}

  # call the CREATE MS method for each device
  order = Order(device_db_id)
  order.command_execute('CREATE', config)

  # convert dict object into json
  content = json.loads(order.content)                    

  Orchestration.update_asynchronous_task_details(*async_update_list, 'Synchronizing device configuration: '+device['id']+'')
  order = Order(device_db_id)
  order.command_synchronize(timeout=60)
  
  # check if the response is OK
  if order.response.ok:
    ret = MSA_API.process_content('ENDED',
                                  f'STATUS: {content["status"]}, \
                                  MESSAGE: {content["message"]}',
                                  context, True)
  else:
    ret = MSA_API.process_content('FAILED',
                                  f'Configuration update failed \
                                  - {order.content}',
                                  context, True)

print(ret)