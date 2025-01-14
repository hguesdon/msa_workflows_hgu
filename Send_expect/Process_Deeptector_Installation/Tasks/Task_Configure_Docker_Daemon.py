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


execute_command = " sudo cp daemon.json /etc/docker/daemon.json "
cmd_ret = device.execute_command_on_device(execute_command)
cmd_ret_array = json.loads(device.content)
context.update(docker_daemon_json=cmd_ret_array['result'])

execute_command = " sudo mkdir -p /etc/systemd/system/docker.service.d "
cmd_ret = device.execute_command_on_device(execute_command)
cmd_ret_array = json.loads(device.content)
context.update(mkdir_docker=cmd_ret_array['result'])

execute_command = " sudo cp override.conf /etc/systemd/system/docker.service.d/override.conf "
cmd_ret = device.execute_command_on_device(execute_command)
cmd_ret_array = json.loads(device.content)
context.update(docker_override=cmd_ret_array['result'])

execute_command = " sudo systemctl daemon-reload "
cmd_ret = device.execute_command_on_device(execute_command)
cmd_ret_array = json.loads(device.content)
context.update(daemon_reload=cmd_ret_array['result'])

execute_command = " sudo systemctl restart docker "
cmd_ret = device.execute_command_on_device(execute_command)
cmd_ret_array = json.loads(device.content)
context.update(docker_restart_daemon=cmd_ret_array['result'])

MSA_API.task_success('Docker Deamon Configured on ' + context['MEC_node'] + ' Edge device ' , context, True)


