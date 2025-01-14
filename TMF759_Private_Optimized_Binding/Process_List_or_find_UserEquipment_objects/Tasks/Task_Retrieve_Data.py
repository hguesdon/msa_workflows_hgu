import json
import uuid
import time
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order
import requests


# List all the parameters required by the task
dev_var = Variables()

dev_var.add('ue.0.id', var_type='String')
dev_var.add('ue.0.name', var_type='String')
dev_var.add('ue.0.href', var_type='String')
dev_var.add('ue.0.description', var_type='String')
dev_var.add('ue.0.operationalState', var_type='String')
dev_var.add('ue.0.note', var_type='String')
dev_var.add('ue.0.type', var_type='String')
dev_var.add('ue.0.schemaLocation', var_type='String')
dev_var.add('ue.0.baseType', var_type='String')

dev_var.add('ue.0.locality', var_type='String')
dev_var.add('ue.0.streetNrLast', var_type='String')
dev_var.add('ue.0.streetSuffix', var_type='String')
dev_var.add('ue.0.msisdn', var_type='String')
dev_var.add('ue.0.imsi', var_type='String')
dev_var.add('ue.0.ipv4Address', var_type='String')


context = Variables.task_call(dev_var)

if not context['ue_list_response'] or "ue_list_response" not in context:
	MSA_API.task_error("ue_list_response not found",context, True)

##### Access ca list array
get_list = context['ue_list_response']

ue=[]
context['ue']=[]
# Iterate over each specification
for array in get_list:
	# Access the key and value of each specification
	id = array["id"]
	name = array["name"]
	href = array["href"]
	#description = array["description"]
	description = " "
	operationalState = array["operationalState"]
	#note = array["note"][0]["text"]
	note = " "
	type = array["@type"]
	#schemaLocation = array["@schemaLocation"]
	baseType = array["@baseType"]
	
	#locality=array["place"][0]["place"]["locality"]
	#streetNrLast=array["place"][0]["place"]["streetNrLast"]
	#streetSuffix=array["place"][0]["place"]["streetSuffix"]
	
	locality=" "
	streetNrLast= " "
	streetSuffix=" "
	
	msisdn = array["resourceCharacteristic"][0]["value"]
	imsi = array["resourceCharacteristic"][1]["value"]
	ipv4Address = array["resourceCharacteristic"][2]["value"]
	ue.append(dict(id=id,name=name,href=href,description=description,operationalState=operationalState,note=note,type=type,
	baseType=baseType,locality=locality,streetNrLast=streetNrLast,streetSuffix=streetSuffix,msisdn=msisdn,imsi=imsi,ipv4Address=ipv4Address))
	
context['ue']=ue


MSA_API.task_success("OK",context, True)

