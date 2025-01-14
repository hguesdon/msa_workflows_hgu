import json
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order

dev_var = Variables()
dev_var.add('Degree1', var_type='Device')
dev_var.add('SRG1', var_type='Device')
dev_var.add('Degree2', var_type='Device')
dev_var.add('SRG2', var_type='Device')
context = Variables.task_call(dev_var)

ret = MSA_API.process_content('ENDED',
                                  f'SUCCESSFULLY',
                                  context, True)

print(ret)
