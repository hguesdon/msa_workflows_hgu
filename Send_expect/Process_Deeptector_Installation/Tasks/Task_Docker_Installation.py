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


execute_command = " sudo docker version "
cmd_ret = device.execute_command_on_device(execute_command)
context['execute_command_result'] = device.content
cmd_ret_array = json.loads(device.content)

if (cmd_ret_array['status'] != 'OK'):
	MSA_API.task_error('Error in sending the command to MEC device =' + context['MEC_node'] + ' return=' + cmd_ret, context, True)
else:
	result = "KO"
	context.update(device_push_conf_ret=cmd_ret_array['result'])
	if cmd_ret_array['result']:
		match = re.search('Version:(.*)\n', cmd_ret_array['result'])
		if match:
			context['docker_version'] = match.group(1)
			MSA_API.task_success('MEC device ' + context['MEC_node'] + ' is already running docker : ' + context['docker_version'], context, True)
			result = "OK"
		else:
			execute_command = " curl -fsSL https://get.docker.com -o get-docker.sh "
			Orchestration.update_asynchronous_task_details(*async_update_list, 'curl -fsSL https://get.docker.com -o get-docker.sh')
			cmd_ret = device.execute_command_on_device(execute_command)
			cmd_ret_array = json.loads(device.content)
			context.update(curl_docker_sh=cmd_ret_array['result'])
			execute_command = " sudo -E sh get-docker.sh "
			Orchestration.update_asynchronous_task_details(*async_update_list, 'sudo -E sh get-docker.sh')
			cmd_ret = device.execute_command_on_device(execute_command)
			cmd_ret_array = json.loads(device.content)
			context.update(docker_sh=cmd_ret_array['result'])
			execute_command = " rm get-docker.sh "
			Orchestration.update_asynchronous_task_details(*async_update_list, 'rm get-docker.sh')
			cmd_ret = device.execute_command_on_device(execute_command)
			cmd_ret_array = json.loads(device.content)
			context.update(rm_docker_sh=cmd_ret_array['result'])
			execute_command = " sudo systemctl --now enable docker "
			Orchestration.update_asynchronous_task_details(*async_update_list, 'sudo systemctl --now enable docker')
			cmd_ret = device.execute_command_on_device(execute_command)
			cmd_ret_array = json.loads(device.content)
			context.update(docker_enable=cmd_ret_array['result'])
			execute_command = " sudo systemctl start docker "
			Orchestration.update_asynchronous_task_details(*async_update_list, 'sudo systemctl start docker')
			cmd_ret = device.execute_command_on_device(execute_command)
			cmd_ret_array = json.loads(device.content)
			context.update(docker_start=cmd_ret_array['result'])
			execute_command = " sudo docker version "
			Orchestration.update_asynchronous_task_details(*async_update_list, 'sudo docker version')
			cmd_ret = device.execute_command_on_device(execute_command)
			cmd_ret_array = json.loads(device.content)
			context.update(docker_version=cmd_ret_array['result'])
			if cmd_ret_array['result']:
				match = re.search('Version:(.*)\n', cmd_ret_array['result'])
				if match:
					context['docker_version'] = match.group(1)
					MSA_API.task_success('MEC device ' + context['MEC_node'] + ' is running docker : ' + context['docker_version'], context, True)
					result = "OK"


if (result != 'OK'):
    MSA_API.task_error('Can not install docker on MEC device =' + context['MEC_node'] + ' return=' + cmd_ret_array['result'], context, True)
else:
	MSA_API.task_success('Edge device ' + context['MEC_node'] + ' is running : ' + context['docker_version'], context, True)


