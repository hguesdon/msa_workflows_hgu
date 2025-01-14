from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order
from msa_sdk import constants
import time
from msa_sdk.orchestration import Orchestration
import re 
import json
import uuid

dev_var = Variables()
dev_var.add('billingAccount', var_type='String')
dev_var.add('priority', var_type='Integer')
dev_var.add('sST', var_type='Integer');
dev_var.add('availability', var_type='String')
dev_var.add('dLLatency', var_type='String')
dev_var.add('uLLatency', var_type='String')
dev_var.add('dLThptPerUE', var_type='String')
dev_var.add('uLThptPerUE', var_type='String')
dev_var.add('coverageArea', var_type='String')
dev_var.add('maxNumberofUEs', var_type='Integer')
context = Variables.task_call(dev_var)

'''
This task should call remotely one of the push configuration workflow

'''

def get_process_instance(orch, process_id, timeout = 600, interval=5):
    response = {}
    global_timeout = time.time() + timeout
    while True:
        #get service instance execution status.
        orch.get_process_instance(process_id)
        response = json.loads(orch.content)
        status = response.get('status').get('status')
        #context.update(get_process_instance=status)
        if status != constants.RUNNING or time.time() > global_timeout:
            break
        time.sleep(interval)

    return response

#if int(context['Criticality']) == 3:
if int(context['priority']) < int(context['Criticality']) :
	MSA_API.task_error('Priority : '+context['priority']+' lower than Criticality : '+context['Criticality']+', No 5G Slice created', context, True)


#Initiate orchestraction object.
ubiqube_id=context['UBIQUBEID']
orch = Orchestration(ubiqube_id)

SERVICE_NAME = 'Process/workflows/5G_Slices/5G_Slices'
CREATE_PROCESS_NAME = 'Process/workflows/5G_Slices/Process_New_Slice'
service_id = ''

'''
data example 
{
  "billingAccount": "166",
  "priority": "2",
  "sST": "1",
  "availability": "99.999%",
  "dLLatency": "10ms",
  "uLLatency": "10ms",
  "dLThptPerUE": "100Mb",
  "uLThptPerUE": "100Mb",
  "coverageArea": "TEST",
  "maxNumberofUEs": "3"
}

'''


data = dict(billingAccount = context['billingAccount'],
  priority = context['priority'],
  sST = context['sST'],
  availability = context['availability'],
  dLLatency = context['dLLatency'],
  uLLatency = context['uLLatency'],
  dLThptPerUE = context['dLThptPerUE'],
  uLThptPerUE = context['uLThptPerUE'],
  coverageArea = context['coverageArea'],
  maxNumberofUEs = context['maxNumberofUEs']
	)
	
orch.execute_service(SERVICE_NAME, CREATE_PROCESS_NAME, data)
response = json.loads(orch.content)
context['response'] = response

service_id = response.get('serviceId').get('id')
process_id = response.get('processId').get('id')
#get service process details.
response = get_process_instance(orch, process_id)
status = response.get('status').get('status')
details = response.get('status').get('details')

if 'serviceId' in response:
	service_id = response.get('serviceId').get('id')
	service_ext_ref = response.get('serviceId').get('serviceExternalReference')
	#Store service_instance_id 5G WF in context.
	context['5G_creation_service_instance'] = dict(external_ref=service_ext_ref, instance_id=service_id)
else:
	MSA_API.task_error('Missing service id return by orchestration operation.', context, True)

if status == constants.FAILED:
	MSA_API.task_error('Execute 5G Slices WF service operation failed: ' + details + ' (#' + str(service_id) + ')', context, True)
	
MSA_API.task_success('5G Slice created successfully', context, True)
