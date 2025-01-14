from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order
from msa_sdk.device import Device
from msa_sdk.orchestration import Orchestration
from msa_sdk.customer import Customer
from msa_sdk import util

from datetime import datetime
from msa_sdk import constants
import re
import json
import sys
import time


dev_var = Variables()

dev_var.add('vpnConcentratorId', var_type='String')
dev_var.add('ME_name', var_type='String')
dev_var.add('ME_IP', var_type='String')
dev_var.add('ME_login', var_type='String')
dev_var.add('ME_password', var_type='String')

context = Variables.task_call(dev_var)

CurrentDevice = Device(customer_id = re.match('^\D+?(\d+?)$',context['UBIQUBEID']).group(1),
                        name = context['ME_name'],
                        manufacturer_id = '14020601',
                        model_id = '14020601',
                        login = context['ME_login'],
                        password = context['ME_password'],
                        password_admin = context['ME_password'],
                        management_address = context['ME_IP'] 
                        )
CurrentDevice.create()
CurrentDevice.read()

context['ME_id'] = CurrentDevice.device_id

CurrentDevice.activate()

ret = MSA_API.process_content('ENDED', 'Task OK', context, True)
print(ret)

