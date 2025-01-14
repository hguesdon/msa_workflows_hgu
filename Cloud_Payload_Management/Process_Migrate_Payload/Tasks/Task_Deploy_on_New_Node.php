<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args()
{
 // create_var_def('new_destination', 'Device');

}

check_mandatory_param('new_destination');

$device_id = $context['new_destination'];
$prefix = substr($device_id, 0, 3);
$device_id = str_replace($prefix, '', $device_id);
$object_id=$context['payload_descriptor'];


$obj_params=array();
$obj_params['object_id']=$object_id;
$obj_params['status']= 'active';

$cmd_obj=array("App_Deployment"=>array("$object_id" => $obj_params));


$response = execute_command_and_verify_response($device_id, "CREATE", $cmd_obj, "CREATE App_Deployment");
  $response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = prepare_json_response($response['wo_status'], $response['wo_comment'], $context, true);
	echo $response;
	exit;
}
$my_dc=$context['k8_device_id'];
if($my_dc === 'UBI1270'){
    $context['dc_id'] = 'X';
}elseif ($my_dc === 'UBI1654'){
    $context['dc_id'] = 'X';
}elseif ($my_dc === 'UBI1654'){
    $context['dc_id'] = 'Z';
}
$response = prepare_json_response(ENDED, "Deployment on target Successful",$context, true);
echo $response;
?>
