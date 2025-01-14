
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

dev_var = Variables()
dev_var.add('ServiceID', var_type='String')
dev_var.add('description', var_type='String')
dev_var.add('priority', var_type='String')
dev_var.add('SwInfo', var_type='String')
dev_var.add('availability', var_type='String')
dev_var.add('DL_latency', var_type='String')
dev_var.add('DL_ThptPerUE', var_type='String')
dev_var.add('maxNumberOfUEs', var_type='String')
dev_var.add('UserStorageVolume', var_type='String')
dev_var.add('billingAccount', var_type='String')
dev_var.add('externalId', var_type='String')
dev_var.add('serviceOrderId', var_type='String')


context = Variables.task_call(dev_var)


ret = MSA_API.process_content('ENDED', 'Service Instantiated', context, True)
print(ret)

