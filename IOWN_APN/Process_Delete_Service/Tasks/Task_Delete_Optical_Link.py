
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API


dev_var = Variables()
dev_var.add('freq', var_type='String')
dev_var.add('start', var_type='Integer')
dev_var.add('end', var_type='Integer')
context = Variables.task_call(dev_var)

ret = MSA_API.process_content('ENDED', 'Service Deleted', context, True)
print(ret)

