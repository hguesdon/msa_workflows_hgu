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
execute_command = " lsb_release -a "
cmd_ret = device.execute_command_on_device(execute_command)
cmd_ret_array = json.loads(device.content)
context.update(os_check=cmd_ret_array['result'])


if (cmd_ret_array['status'] != 'OK'):
	MSA_API.task_error('Error in sending the command to MEC device =' + context['MEC_node'] + ' return=' + cmd_ret, context, True)
else:
	result = "KO"
	if cmd_ret_array['result']:
		match = re.search('Description:\t(.+?)\n', cmd_ret_array['result'])
		if match:
			context['os'] = match.group(1)
			result = "OK"

if (result != 'OK'):
    MSA_API.task_error('Can not get OS version on MEC device =' + context['MEC_node'] + ' return=' + cmd_ret_array['result'], context, True)
else:
	MSA_API.task_success('Edge device ' + context['MEC_node'] + ' is running : ' + context['os'], context, True)


