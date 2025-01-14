'''
Visit http://[YOUR_MSA_URL]/msa_sdk/ to see what you can import.
'''
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
import time

dev_var = Variables()

time.sleep(5)
ret = MSA_API.process_content('ENDED', 'Task OK', context, True)
print(ret)

