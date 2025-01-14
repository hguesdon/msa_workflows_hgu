from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API


dev_var = Variables()
dev_var.add('pe_1_policy_map.0.policy_map', var_type='String')
dev_var.add('pe_1_policy_map.0.class_map', var_type='String')
dev_var.add('pe_1_policy_map.0.value', var_type='String')
dev_var.add('pe_1_policy_map.0.rate', var_type='String')

dev_var.add('pe_1_interface.0.name', var_type='String')
dev_var.add('pe_1_interface.0.description', var_type='String')
dev_var.add('pe_1_interface.0.vlan_id', var_type='String')
dev_var.add('pe_1_interface.0.address', var_type='String')
dev_var.add('pe_1_interface.0.mask', var_type='String')
dev_var.add('pe_1_interface.0.policy_map_in', var_type='String')
dev_var.add('pe_1_interface.0.policy_map_out', var_type='String')

dev_var.add('pe_1_prefix_list.0.list_name', var_type='String')
dev_var.add('pe_1_prefix_list.0.action', var_type='String')
dev_var.add('pe_1_prefix_list.0.address', var_type='String')

dev_var.add('pe_1_route_map.0.route_map', var_type='String')
dev_var.add('pe_1_route_map.0.action', var_type='String')
dev_var.add('pe_1_route_map.0.prefix_list', var_type='String')

dev_var.add('pe_1_bgp.0.bgp_as', var_type='String')
dev_var.add('pe_1_bgp.0.neighbor', var_type='String')
dev_var.add('pe_1_bgp.0.remote_as', var_type='String')
dev_var.add('pe_1_bgp.0.route_map', var_type='String')

dev_var.add('cMETRO_1_vlan.0.vlan_id', var_type='String')
dev_var.add('cMETRO_1_vlan.0.name', var_type='String')

dev_var.add('cMETRO_1_policy_map.0.policy_map', var_type='String')
dev_var.add('cMETRO_1_policy_map.0.cls_map', var_type='String')
dev_var.add('cMETRO_1_policy_map.0.bps', var_type='String')
dev_var.add('cMETRO_1_policy_map.0.byte', var_type='String')

dev_var.add('cMETRO_1_interface.0.name', var_type='String')
dev_var.add('cMETRO_1_interface.0.description', var_type='String')
dev_var.add('cMETRO_1_interface.0.mode', var_type='String')
dev_var.add('cMETRO_1_interface.0.vlan', var_type='String')
dev_var.add('cMETRO_1_interface.0.policy_map_in', var_type='String')
dev_var.add('cMETRO_1_interface.0.policy_map_out', var_type='String')

context = Variables.task_call(dev_var)

ret = MSA_API.process_content('ENDED', 'OK', context, True)
print(ret)