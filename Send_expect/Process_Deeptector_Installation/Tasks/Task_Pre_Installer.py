import json
import re
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.device import Device

dev_var = Variables()
dev_var.add('MEC_node', var_type='Device')
context = Variables.task_call(dev_var)

mec = context['MEC_node'][3:]
device = Device(device_id=mec)


execute_command = " sudo -E install/preinstaller --yes "
#execute_command = " ll install/preinstaller "
cmd_ret = device.execute_command_on_device(execute_command)
cmd_ret_array = json.loads(device.content)
context.update(pre_installer=cmd_ret_array['result'])


MSA_API.task_success('Deeptector preinstalled on ' + context['MEC_node'] + ' Edge device ' , context, True)


