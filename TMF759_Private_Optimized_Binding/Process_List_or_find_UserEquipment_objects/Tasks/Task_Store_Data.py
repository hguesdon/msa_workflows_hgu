import json
import uuid
import time
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order
import requests
import datetime 

# List all the parameters required by the task
dev_var = Variables()

context = Variables.task_call(dev_var)
#MSA_API.task_success('OK SKIP TEST',context, True)

username = 'superuser'
password = 'x^ZyuGM6~u=+fY2G'

# Get the current date
current_date = datetime.datetime.now()
# Format the date as YYYY-MM-DD
formatted_date = current_date.strftime("%Y-%m-%d")

# Generate the index name
index_name = f"ubi-tmf759-compliant-{formatted_date}"

#url = 'http://msa-es:9200/ubi-tmf628/_doc'
url = 'http://msa-es:9200/'+index_name+'/_doc'

headers = {'Content-Type': 'application/json'} 

# Clean tmf759 Elasticsearch index for ue
urldelete = 'http://msa-es:9200/ubi-tmf759-compliant-*/_doc/_delete_by_query'
headers = {'Content-Type': 'application/json'}
data = {
  "query": {
    "match": {
      "type": "UserEquipment"
    }
  }
}
request = requests.post(urldelete, auth=(username, password), headers=headers,  json=data)
context['delete_ue_es_index_response']=request.json()

# Iterate through search results
for result in context['ue']:
    # Add date key and value
    result["request_time"] = datetime.datetime.utcnow().isoformat() + 'Z'
    result["customer_id"]=19

    # Index the document in Elasticsearch
    request = requests.post(url, auth=(username, password), headers=headers, data=json.dumps(result))
    #es.index(index='your_index_name', doc_type='your_doc_type', body=result)

    context['data_store_response']=request.json()

MSA_API.task_success(context['data_store_response'],context, True)
