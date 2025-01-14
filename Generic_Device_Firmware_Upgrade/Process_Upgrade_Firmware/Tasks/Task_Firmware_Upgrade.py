"""
Visit http://[YOUR_MSA_URL]/msa_sdk/ to see what you can import.
"""

import json
import time

from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk import constants
from msa_sdk.msa_api import MSA_API
from msa_sdk.lookup import Lookup
from msa_sdk.customer import Customer
from msa_sdk.device import Device
from msa_sdk.orchestration import Orchestration


dev_var = Variables()
dev_var.add('customer_devices.0.to_update', var_type='Boolean')
dev_var.add('customer_devices.0.name', var_type='String')
dev_var.add('customer_devices.0.externalReference', var_type='String')
dev_var.add('customer_devices.0.device_type', var_type='String')
dev_var.add('firmware_file', var_type='File')

context = Variables.task_call(dev_var)

#Create Orchestration object to update GUI dynamically
Orchestration = Orchestration(context['UBIQUBEID'])
async_update_list = (context['PROCESSINSTANCEID'], context['TASKID'], context['EXECNUMBER'])


# get all devices for the customer
lookup = Lookup()
customer = Customer()

# Get Subtenant external reference
ubiqube_id = context["UBIQUBEID"]  #  = "SYZA11"
customer_int = ubiqube_id[4:]  #  = "11"
customer_detail = customer.get_customer_by_id(customer_int)

context["customer_detail"] = str(customer_detail)
customer_detail = json.loads(customer_detail)

customer_ext_ref = customer_detail["externalReference"]

lookup.look_list_device_by_customer_ref(customer_ext_ref)
all_devices = lookup.response.json()


context["all_devices"] = str(all_devices)
customer_devices = []

devices_updated = []

for device in all_devices:

    device1 = {}
    device1["ubiId"] = device["ubiId"]
    device1["name"] = device["name"]
    device1["externalReference"] = device["externalReference"]
    customer_devices.append(device1)

context["customer_devices"] = customer_devices
nb_devices = len(customer_devices)

for i in range(len(customer_devices)):
  customer_device = customer_devices[i]
  if customer_device.get('to_update') and customer_device['to_update']: 
    device_id = customer_device['ubiId'][3:]  # 'SYZ152'
    device = Device(device_id=device_id)
    context['device_id'] = device_id
    params='FILE='+'/opt/fmc_repository/'+context['firmware_file']
    res = device.update_firmware(params)
    start_update_firmware =  json.loads(device.content)
    context['start_update_firmware_res'] = str(res)
    context['start_update_firmware'] = start_update_firmware 
    
    if start_update_firmware.get('wo_status') and start_update_firmware['wo_status'] !=  "END" :
      MSA_API.task_error('Devices firmware updated failed  ' +  start_update_firmware['wo_newparams'], context, True) 
    
    status = 'RUNNING'
    loop   = 0
    while status == 'RUNNING' and loop < 200:
      time.sleep(5)
      response = device.get_update_firmware_status()
      status = response.get('status')
      loop = loop + 1
      Orchestration.update_asynchronous_task_details(*async_update_list, 'Firmware upgrade message '+response['message'])
      
    context['update_firmware_status']  =   response  
    if status !=  "ENDED" :
      MSA_API.task_error('Devices firmware updated failed with status '+ status+ ', response :' + str(response), context, True)
    devices_updated.append(customer_device.get('name'))

if devices_updated:
  MSA_API.task_success('Firmware updated for devices (' + ' ,'.join(devices_updated) + ')', context, True) 
else:
  MSA_API.task_success('No Devices selected to update', context, True) 
