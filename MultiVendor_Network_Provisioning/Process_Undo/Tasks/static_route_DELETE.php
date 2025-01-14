<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args()
{
  create_var_def('devices.0.device_id', 'Device');
  create_var_def('static_route.0.object_id', 'AutoIncrement');
create_var_def('static_route.0.dest', 'String');
create_var_def('static_route.0.mask', 'String');
create_var_def('static_route.0.gw', 'String');

}

foreach($context['devices'] as $device){
    
$device_id = $device['device_id'];
$prefix = substr($device_id, 0, 3);
$device_id = str_replace($prefix, '', $device_id);

foreach ($context['static_route'] as $key => $value) {
   $object_parameters['static_route'][$value['object_id']] = $value;
}


$response = execute_command_and_verify_response($device_id, "DELETE", $object_parameters, "DELETE static_route");
  $response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = prepare_json_response($response['wo_status'], $response['wo_comment'], $context, true);
	echo $response;
	exit;
}
}
$response = prepare_json_response(ENDED, "order command execute successfull", $response['wo_newparams'], true);
echo $response;
?>
