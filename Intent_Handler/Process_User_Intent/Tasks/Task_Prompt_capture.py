import requests
import json
#import openai
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

dev_var = Variables()
dev_var.add('prompt', var_type='String')
dev_var.add('answer', var_type='String')

context = Variables.task_call(dev_var)
prompt = context['prompt']
api_key=""

'''
def query_gpt(prompt, model="gpt-3.5-turbo", max_tokens=150):
    openai.api_key = ''

    try:
        response = openai.Completion.create(
            engine=model,
            prompt=prompt,
            max_tokens=max_tokens
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return str(e)
        
'''

def query_openai_gpt(prompt, model="text-davinci-003", api_key=""):
    url = "https://api.openai.com/v1/engines/{}/completions".format(model)

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "prompt": prompt,
        "max_tokens": 150
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json().get('choices')[0].get('text').strip()
    else:
        return "Error: " + response.text

result = query_openai_gpt(prompt, api_key="")

context['answer'] = result
ret = MSA_API.process_content('ENDED', 'Task OK', context, True)
print(ret)