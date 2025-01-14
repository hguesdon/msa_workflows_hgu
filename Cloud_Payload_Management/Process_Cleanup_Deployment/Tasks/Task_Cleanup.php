<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args()
{

}

check_mandatory_param('k8_device_id');

$device_id = $context['k8_device_id'];
$prefix = substr($device_id, 0, 3);
$device_id = str_replace($prefix, '', $device_id);
$object_id=$context['payload_descriptor'];


$obj_params=array();
$obj_params['object_id']=$object_id;
$obj_params['status']= 'active';

$cmd_obj=array("App_Deployment"=>array("$object_id" => $obj_params));


$response = execute_command_and_verify_response($device_id, "DELETE", $cmd_obj, "CREATE App_Deployment");
  $response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = prepare_json_response($response['wo_status'], $response['wo_comment'], $context, true);
	echo $response;
	exit;
}

$response = prepare_json_response(ENDED, "Deployment cleaned up on existing node", $context,true);
echo $response;
?>
