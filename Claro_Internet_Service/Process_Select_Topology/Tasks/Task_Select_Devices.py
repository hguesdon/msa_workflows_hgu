from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API


dev_var = Variables()
dev_var.add('device_a', var_type='String')
dev_var.add('device_c', var_type='String')
context = Variables.task_call(dev_var)

ret = MSA_API.process_content('ENDED', 'OK', context, True)
print(ret)