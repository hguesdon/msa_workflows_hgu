import json
import re
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.device import Device
from msa_sdk.order import Order

dev_var = Variables()
dev_var.add('MEC_node', var_type='Device')
dev_var.add('compose_pj_name', var_type='String')
dev_var.add('admin_email', var_type='String')
dev_var.add('admin_password', var_type='Password')

context = Variables.task_call(dev_var)

mec = context['MEC_node'][3:]
device = Device(device_id=mec)

#execute_command = " ./deeptector_start.sh "
execute_command = " sudo install/installer --yes --compose_pj_name=" + context['compose_pj_name'] + " --admin_email=" + context['admin_email'] + " --admin_password=" + context['admin_password'] + " --local_dt_root=/opt/deeptector --http_port=80 --https_port=443 --import_engine "
cmd_ret = device.execute_command_on_device(execute_command)
cmd_ret_array = json.loads(device.content)
context.update(deeptector_up=cmd_ret_array['result'])

ms_order = Order(mec)
ms_order.command_synchronize(timeout=60)

MSA_API.task_success('Deeptector installed and running on ' + context['MEC_node'] + ' Edge device ' , context, True)


