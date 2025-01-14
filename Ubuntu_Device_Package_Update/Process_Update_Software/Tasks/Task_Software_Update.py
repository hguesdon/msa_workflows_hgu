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
dev_var.add("customer_devices.0.to_update", var_type="Boolean")
dev_var.add("customer_devices.0.name", var_type="String")
dev_var.add("customer_devices.0.ubiId", var_type="String")
dev_var.add("customer_devices.0.password", var_type="String")
dev_var.add("package_name", var_type="String")

context = Variables.task_call(dev_var)

# Create Orchestration object to update GUI dynamically
Orchestration = Orchestration(context["UBIQUBEID"])
async_update_list = (
    context["PROCESSINSTANCEID"],
    context["TASKID"],
    context["EXECNUMBER"],
)

customer_devices = context["customer_devices"]
devices_updated = []
failed_devices = []
results = []
for i in range(len(customer_devices)):
    customer_device = customer_devices[i]
    if customer_device.get("to_update") and customer_device["to_update"]:
        device_id = customer_device["ubiId"][3:]  # 'SYZ152'
        device = Device(device_id=device_id)
        context["device_id"] = device_id
        password = customer_device.get("password")
        package_name = context["package_name"]
        command = f"echo {password} | sudo -S apt-get update && apt-get install {package_name}"
        result = device.execute_command_on_device(command)
        result = json.loads(json.loads(result))
        if result.get("status") == "FAIL":
            failed_devices.append(customer_device.get("name"))
            results.append(result)
        elif result.get("status") == "OK":
            devices_updated.append(customer_device.get("name"))
            time.sleep(60)
            command = f"which {package_name}"
            result = device.execute_command_on_device(command)
            result = json.loads(json.loads(result))
            results.append(result)

MSA_API.task_success(
    "Successful devices:"
    + " ,".join(devices_updated)
    + "Failed devices:"
    + " ,".join(failed_devices)
    + "Results: "
    + json.dumps(results),
    context,
    True,
)
