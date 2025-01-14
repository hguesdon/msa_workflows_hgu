"""
Visit http://[YOUR_MSA_URL]/msa_sdk/ to see what you can import.
"""

import json

from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk import constants
from msa_sdk.msa_api import MSA_API
from msa_sdk.lookup import Lookup
from msa_sdk.customer import Customer
from msa_sdk.device import Device


dev_var = Variables()
dev_var.add('package_name', var_type='String')

context = Variables.task_call(dev_var)

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

for device in all_devices:

    device1 = {}
    device1["ubiId"] = device["ubiId"]
    device1["name"] = device["name"]
    customer_devices.append(device1)
    devicelongid = device1['ubiId'][3:]
    deviceObj = Device(device_id= devicelongid) 
    device_detail = deviceObj.read()
    device_detail = json.loads(device_detail)
    device1['password'] = device_detail['password']

context["customer_devices"] = customer_devices
context["package_name"] = context['package_name']
nb_devices = len(customer_devices)

MSA_API.task_success('We found ' + str(nb_devices) + ' devices for the current Sub Tenant Id '+str(ubiqube_id), context, True) 
