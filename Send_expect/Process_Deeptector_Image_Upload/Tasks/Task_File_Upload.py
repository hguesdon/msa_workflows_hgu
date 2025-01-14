import json
import os
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.device import Device

dev_var = Variables()
dev_var.add('MEC_node', var_type='Device')
dev_var.add('Deeptector_code', var_type='File')
#dev_var.add('Deeptector_code', var_type='String')
context = Variables.task_call(dev_var)

mec = context['MEC_node'][3:]
device = Device(device_id=mec)
fullpath = context['Deeptector_code']
dst_dir = "/tmp"

file_name = os.path.basename(fullpath)
file_path = "/opt/fmc_repository/" + os.path.dirname(fullpath)
params = { "src_dir": file_path, "file_pattern": file_name, "dst_dir": dst_dir}
ret = device.run_jsa_command_device('send_files', params)

context.update(Image_Upload = ret)

ret = MSA_API.process_content('ENDED', 'Task OK', context, True)
print(ret)


