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


execute_command = " sudo curl -L https://github.com/docker/compose/releases/download/1.28.5/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose "
cmd_ret = device.execute_command_on_device(execute_command)
cmd_ret_array = json.loads(device.content)
context.update(docker_compose=cmd_ret_array['result'])

execute_command = " sudo chmod +x /usr/local/bin/docker-compose "
cmd_ret = device.execute_command_on_device(execute_command)
cmd_ret_array = json.loads(device.content)
context.update(docker_compose=cmd_ret_array['result'])

MSA_API.task_success('Docker compose installed on ' + context['MEC_node'] + ' Edge device ' , context, True)


