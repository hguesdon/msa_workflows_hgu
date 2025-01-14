'''
Visit http://[YOUR_MSA_URL]/msa_sdk/ to see what you can import.
'''
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API


dev_var = Variables()
dev_var.add('agg_term_links.0.agg_rtr', var_type='Device')
dev_var.add('agg_term_links.0.access_node', var_type='Device')
dev_var.add('agg_term_links.0.link', var_type='String')

dev_var.add('agg_dir_link.0.agg_rtr1', var_type='Device')
dev_var.add('agg_dir_link.0.agg_rtr2', var_type='Device')
dev_var.add('agg_dir_link.0.link', var_type='String')

dev_var.add('access_node_link.0.access_node1', var_type='Device')
dev_var.add('access_node_link.0.access_node2', var_type='Device')
dev_var.add('access_node_link.0.link', var_type='String')

dev_var.add('linear_node_links.0.agg_rtr', var_type='Device')
dev_var.add('linear_node_links.0.access_node', var_type='Device')
dev_var.add('linear_node_links.0.link', var_type='String')

dev_var.add('status', var_type='String')
dev_var.add('access_ring_id', var_type='String')
context = Variables.task_call(dev_var)

ret = MSA_API.process_content('ENDED', 'Task OK', context, True)
print(ret)

