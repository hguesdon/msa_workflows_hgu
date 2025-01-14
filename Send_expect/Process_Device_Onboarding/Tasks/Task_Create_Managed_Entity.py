import json
import re
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.device import Device
from msa_sdk.order import Order

dev_var = Variables()
dev_var.add('ME_name', var_type='String')
dev_var.add('ME_address', var_type='String')
dev_var.add('ME_login', var_type='String')
dev_var.add('ME_password', var_type='Password')
dev_var.add('relatedParties.0.role', var_type='String')
dev_var.add('relatedParties.0.id', var_type='String')
dev_var.add('relatedParties.0.name', var_type='String')
context = Variables.task_call(dev_var)

me_managementAddress = context['ME_address']
me_password = context['ME_password']
me_login = context['ME_login']
me_name = context['ME_name']
me_manufacturerId = "14020601"
me_modelId = "14020601"
me_customerid = context['UBIQUBEID'][4:]


device = Device(
            customer_id=me_customerid,
            name=me_name,
            manufacturer_id=me_manufacturerId,
            model_id=me_modelId,
            login=me_login,
            password=me_password,
            password_admin="admin",
            management_address=me_managementAddress,
            management_port="2222",
            device_external="",
            log_enabled=True,
            log_more_enabled=True,
            mail_alerting=True,
            reporting=True,
            snmp_community='ubiqube',
            device_id="")


cmd_ret = device.create()
context.update(me_create=cmd_ret)
device_id = cmd_ret.get('id')
context['MEC_node'] = "UBI"+str(device_id)
context.update(ME_id=device_id)
device.activate()


MSA_API.task_success(' Managed Device '+ context['MEC_node'] +' Created ' , context, True)

