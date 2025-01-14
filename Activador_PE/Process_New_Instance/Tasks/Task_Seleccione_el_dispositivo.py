from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order
from msa_sdk.orchestration import Orchestration
from msa_sdk import util
import json

dev_var = Variables()
dev_var.add('device_id', var_type='Device')
context = Variables.task_call(dev_var)

ret = MSA_API.process_content('ENDED', context, True)
print(ret)