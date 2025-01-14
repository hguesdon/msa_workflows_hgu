<?php

/**
 * This file is necessary to include to use all the in-built libraries of /opt/fmc_repository/Reference/Common
 */
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

/**
 * List all the parameters required by the task
 */
function list_args()
{

}

$billingId=$context['billingAccount'];
$context['URI'] = 'http://4.156.254.135:9876/tmf-api/resourceOrdering/v4/resourceOrder';
$body_request='
{
	"category":"Standard",
	"name":"String",
	"priority":0,
	"action":"add",
	"id":"ab4sdlblj6h2kj9bb",
	"orderItem":
		[
			{
				"id":"xxxxxxxxx",
				"action":"add",
				"resource":
					{
						"id":"xxxxxxxx",
						"description":"MIoT Slice creation",
						"resourceCharacteristic":
							[
								{
									"name":"location",
									"value":"eastus"
								},
								{
									"name":"snssai.sst",
									"value":4
								},
								{
									"name":"sliceName",
									"value":"'.$context['access_location'].'"
								},
								{
									"name":"simPolicyName",
									"value":"'.$context['access_location'].'SimPlolicyName"
								},
								{
									"name":"uplink",
									"value":"1 Gbps"
								},
								{
									"name":"downlink",
									"value":"1 Gbps"
									
								}
							]
					}
			}
		]
	
}';

$ci = curl_init();
    curl_setopt($ci, CURLOPT_URL,$context['URI']);
    curl_setopt($ci, CURLOPT_TIMEOUT, 200);
    curl_setopt($ci, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ci, CURLOPT_FORBID_REUSE, 0);
    curl_setopt($ci, CURLOPT_CUSTOMREQUEST, 'PUT');
    curl_setopt($ci, CURLOPT_POSTFIELDS, $body_request);
    curl_setopt($ci, CURLOPT_HTTPHEADER, array('accept: application/json','Content-Type: application/json'));
    $result= curl_exec($ci);

/* Store the result in a variable      */    
$context['result']=$result;	
task_success("Slice provisioning completed for the billing account: $billingId");
task_error('Task FAILED');
?>
