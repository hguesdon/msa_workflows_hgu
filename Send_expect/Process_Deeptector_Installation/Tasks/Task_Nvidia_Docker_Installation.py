import json
import re
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.device import Device
from msa_sdk.orchestration import Orchestration

dev_var = Variables()
dev_var.add('MEC_node', var_type='Device')
context = Variables.task_call(dev_var)

mec = context['MEC_node'][3:]
device = Device(device_id=mec)

process_id = context['SERVICEINSTANCEID']
Orchestration = Orchestration(context['UBIQUBEID'])
async_update_list = (context['PROCESSINSTANCEID'], context['TASKID'], context['EXECNUMBER'])

execute_command = " distribution=$(. /etc/os-release;echo $ID$VERSION_ID) "
cmd_ret = device.execute_command_on_device(execute_command)
cmd_ret_array = json.loads(device.content)
context.update(distribution=cmd_ret_array['result'])

execute_command = " curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add - "
cmd_ret = device.execute_command_on_device(execute_command)
cmd_ret_array = json.loads(device.content)
context.update(distribution=cmd_ret_array['result'])

execute_command = " curl -s -L   https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list "
cmd_ret = device.execute_command_on_device(execute_command)
cmd_ret_array = json.loads(device.content)
context.update(distribution=cmd_ret_array['result'])

execute_command = " sudo apt-get update "
Orchestration.update_asynchronous_task_details(*async_update_list, 'sudo apt-get update')
cmd_ret = device.execute_command_on_device(execute_command)
cmd_ret_array = json.loads(device.content)
context.update(apt_update=cmd_ret_array['result'])

'''
execute_command = " sudo apt-get install -y nvidia-docker2  "
Orchestration.update_asynchronous_task_details(*async_update_list, 'sudo apt-get install -y nvidia-docker2')
cmd_ret = device.execute_command_on_device(execute_command)
cmd_ret_array = json.loads(device.content)
context.update(apt_install_nvidia_docker2=cmd_ret_array['result'])
'''
execute_command = " sudo apt-get install -y nvidia-container-toolkit   "
Orchestration.update_asynchronous_task_details(*async_update_list, 'sudo apt-get install -y nvidia-container-toolkit')
cmd_ret = device.execute_command_on_device(execute_command)
cmd_ret_array = json.loads(device.content)
context.update(apt_install_nvidia_toolkit=cmd_ret_array['result'])

execute_command = " sudo apt-get install -y nvidia-contianer-runtime  "
Orchestration.update_asynchronous_task_details(*async_update_list, 'sudo apt-get install -y nvidia-container-runtime')
cmd_ret = device.execute_command_on_device(execute_command)
cmd_ret_array = json.loads(device.content)
context.update(apt_install_nvidia_runtime=cmd_ret_array['result'])

execute_command = " sudo systemctl restart docker "
Orchestration.update_asynchronous_task_details(*async_update_list, 'sudo systemctl restart docker')
cmd_ret = device.execute_command_on_device(execute_command)
cmd_ret_array = json.loads(device.content)
context.update(docker_restart=cmd_ret_array['result'])

MSA_API.task_success('Nvidia packaged installed on ' + context['MEC_node'] + ' Edge device ' , context, True)


