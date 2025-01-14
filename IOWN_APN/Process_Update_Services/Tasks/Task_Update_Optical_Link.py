
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

dev_var = Variables()
dev_var.add('freq', var_type='String')
dev_var.add('start', var_type='Integer')
dev_var.add('end', var_type='Integer')
context = Variables.task_call(dev_var)

freq =  context['freq']
start = context['start']
end = context['end']
username = "airflow"
password = "airflow"

url = "http://172.25.100.170:8080/api/v1/dags/change_subPath/dagRuns"

headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json'
}

data = {
    "conf": {
        "freq": freq,
        "start": start,
        "end":  end
    }
}

ret = MSA_API.process_content('ENDED', 'Service Instantiated', context, True)
print(ret)
