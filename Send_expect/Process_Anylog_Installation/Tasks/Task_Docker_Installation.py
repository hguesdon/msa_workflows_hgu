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


execute_command = " docker login --username anyloguser --password anylogpassword "
cmd_ret = device.execute_command_on_device(execute_command)
cmd_ret_array = json.loads(device.content)
context.update(docker_login=cmd_ret_array['result'])

execute_command = " bash deployments/docker-compose/docker_install.sh "
cmd_ret = device.execute_command_on_device(execute_command)
cmd_ret_array = json.loads(device.content)
context.update(docker_install=cmd_ret_array['result'])

MSA_API.task_success('Anylog containers installed ' + context['MEC_node'] + ' MEC device ' , context, True)


