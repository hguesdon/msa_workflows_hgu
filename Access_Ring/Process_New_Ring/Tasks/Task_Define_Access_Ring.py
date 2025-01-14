'''
Visit http://[YOUR_MSA_URL]/msa_sdk/ to see what you can import.
'''
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

'''
List all the parameters required by the task

You can use var_name convention for your variables
They will display automaticaly as "Var Name"
The allowed types are:
  'String', 'Boolean', 'Integer', 'Password', 'IpAddress',
  'IpMask', 'Ipv6Address', 'Composite', 'OBMFRef', 'Device'

 Add as many variables as needed
'''
dev_var = Variables()
dev_var.add('agg_term_link1.0.agg_rtr', var_type='Device')
dev_var.add('agg_term_link1.0.access_node', var_type='Device')
dev_var.add('test', var_type='Device')
ret = MSA_API.process_content('ENDED', 'Access Ring Created', context, True)
print(ret)

