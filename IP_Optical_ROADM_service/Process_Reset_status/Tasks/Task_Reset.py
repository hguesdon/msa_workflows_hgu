import json
import re
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.device import Device

dev_var = Variables()
dev_var.add('device_id', var_type='Device')
context = Variables.task_call(dev_var)

mec = context['device_id'][3:]
device = Device(device_id=mec)


execute_command = " /tmp/ANHL_reset_optical.sh "
cmd_ret = device.execute_command_on_device(execute_command)
cmd_ret_array = json.loads(device.content)
context.update(pre_installer=cmd_ret_array['result'])


MSA_API.task_success('Reset done' , context, True)


