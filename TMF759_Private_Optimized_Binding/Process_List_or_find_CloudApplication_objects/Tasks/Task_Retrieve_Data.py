import json
import uuid
import time
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order
import requests


# List all the parameters required by the task
dev_var = Variables()

dev_var.add('ca.0.id', var_type='String')
dev_var.add('ca.0.name', var_type='String')
dev_var.add('ca.0.href', var_type='String')
dev_var.add('ca.0.operationalState', var_type='String')
dev_var.add('ca.0.note', var_type='String')
dev_var.add('ca.0.type', var_type='String')
dev_var.add('ca.0.schemaLocation', var_type='String')
dev_var.add('ca.0.baseType', var_type='String')
dev_var.add('ca.0.cloudProvider', var_type='String')
dev_var.add('ca.0.cloudRegion', var_type='String')
dev_var.add('ca.0.cloudReference', var_type='String')
dev_var.add('ca.0.ipv4Address', var_type='String')


context = Variables.task_call(dev_var)

if not context['ca_list_response'] or "ca_list_response" not in context:
	MSA_API.task_error("ca_list_response not found",context, True)

##### Access ca list array
get_list = context['ca_list_response']
ca=[]
context['ca']=[]
# Iterate over each specification
for array in get_list:
	# Access the key and value of each specification
	id = array["id"]
	name = array["name"]
	href = array["href"]
	operationalState = array["operationalState"]
	#note = array["note"][0]["text"]
	note = " "
	type = array["@type"]
	#schemaLocation = array["@schemaLocation"]
	baseType = array["@baseType"]
	cloudProvider = array["resourceCharacteristic"][0]["value"]
	cloudRegion = array["resourceCharacteristic"][1]["value"]
	cloudReference = array["resourceCharacteristic"][2]["value"]
	#ipv4Address = array["resourceCharacteristic"][3]["value"]
	ca.append(dict(id=id,name=name,href=href,operationalState=operationalState,note=note,type=type,
	baseType=baseType,cloudProvider=cloudProvider,cloudRegion=cloudRegion,cloudReference=cloudReference))
	
context['ca']=ca


MSA_API.task_success(context['ca'],context, True)

