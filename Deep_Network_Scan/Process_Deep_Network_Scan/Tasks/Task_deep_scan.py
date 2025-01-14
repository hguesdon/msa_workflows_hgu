from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
import subprocess
import nmap
import re
import json

dev_var = Variables()
dev_var.add('hosts.0.ip_address', var_type='IP Address')
dev_var.add('snmp_communities.0.name', var_type='String')
dev_var.add('nmapflag', var_type='Boolean')

context = Variables.task_call(dev_var)
hosts = context['hosts']
communities = context.get('snmp_communities', {})

i = 0
context['hosts'] = dict()
for host in hosts:
    ipAdd = host['ip_address']
    context['hosts'][i] = dict()
    context['hosts'][i]['ip_address'] = ipAdd
    context['hosts'][i]['vendor'] = "SNMP not configured"
    context['hosts'][i]['model'] = "nmap disabled"
    context['hosts'][i]['raw'] = ""
    snmp_success = False
    for community in communities:
        community_name = community['name']
        process = subprocess.Popen(['snmpwalk', '-v', '2c', '-c', community_name, ipAdd, '1.3.6.1.2.1.1.1.0'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = process.communicate()[0]
        if process.returncode is 0:
            context['hosts'][i] = dict()
            context['hosts'][i]['ip_address'] = ipAdd
            info = output.decode().split('=')
            result = re.match('\sSTRING:\s(\S+)\s(\S+)', info[1])
            if result:
                context['hosts'][i]['vendor'] = result.group(1)
                context['hosts'][i]['model'] = result.group(2)
                context['hosts'][i]['raw'] = info[1]
                snmp_success = True
            break
    if not snmp_success and context['nmapflag'] == True:
        nm = nmap.PortScanner()
        machine = nm.scan(ipAdd, arguments='-O', sudo=True)
        if bool(machine['scan'][ipAdd]['osmatch']):
            context['hosts'][i] = dict()
            context['hosts'][i]['ip_address'] = ipAdd
            context['hosts'][i]['vendor'] = machine['scan'][ipAdd]['osmatch'][0]['osclass'][0]['vendor']
            context['hosts'][i]['model'] = machine['scan'][ipAdd]['osmatch'][0]['osclass'][0]['osfamily']
            context['hosts'][i]['raw'] = json.dumps(machine['scan'])
    i += 1        

ret = MSA_API.process_content('ENDED', 'Task OK', context, True)
print(ret)
