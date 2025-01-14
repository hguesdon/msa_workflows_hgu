import json
import re
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.device import Device
from msa_sdk.order import Order

dev_var = Variables()
dev_var.add('MEC_node', var_type='Device')
context = Variables.task_call(dev_var)

mec = context['MEC_node'][3:]
device = Device(device_id=mec)


#execute_command = " cd deployments/docker-compose/demo-cluster-deployment; docker-compose up -d "
execute_command = " ./anylogstop.sh "
cmd_ret = device.execute_command_on_device(execute_command)
cmd_ret_array = json.loads(device.content)
context.update(anylog_up=cmd_ret_array['result'])

#execute_command = " cd lfedge-code/edgex; docker-compose up -d "
execute_command = " ./edgexstop.sh "
cmd_ret = device.execute_command_on_device(execute_command)
cmd_ret_array = json.loads(device.content)
context.update(edgex_up=cmd_ret_array['result'])

ms_order = Order(mec)
ms_order.command_synchronize(timeout=60)

MSA_API.task_success('Anylog is stopped ' + context['MEC_node'] + ' MEC device ' , context, True)


