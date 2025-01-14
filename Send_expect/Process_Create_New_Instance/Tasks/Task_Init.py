from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

dev_var = Variables()
dev_var.add('MEC_node', var_type='Device')
dev_var.add('externalId', var_type='String')
dev_var.add('relatedParties.0.role', var_type='String')
dev_var.add('relatedParties.0.id', var_type='String')
dev_var.add('relatedParties.0.name', var_type='String')
context = Variables.task_call(dev_var)

ret = MSA_API.process_content('ENDED', f'Workflow instance created', context, True)
print(ret)


