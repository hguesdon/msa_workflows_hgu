<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args()
{
  create_var_def('k8_device_id', 'Device');

}
/*$serv_id=$context['vpn_service'];
$vpn_health='';
//Check the VPN health and if active proceed or lese fail the deploy payload process
$resp=_orchestration_get_service_variables_by_service_id ($serv_id);
$resp=json_decode($resp,true);
//logToFile(debug_dump($resp,"**************Response**********\n"));
$item=$resp['wo_newparams'];
foreach($item as $key => $val){
    if($val['name'] === 'health'){
        $vpn_health=$val['value'];
        logToFile ("kekek: $vpn_health");
        break;
        }
}
if(empty($vpn_health)){
   task_error("VPN Service is not provisioned for this DC Service");
} 
if($vpn_health !== 'active'){
    task_error("VPN Not working for this DC Service");
}

*/
check_mandatory_param('k8_device_id');

$device_id = $context['k8_device_id'];
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
$context['best_node']=$context['k8_device_id'];
$my_dc=$context['k8_device_id'];
if($my_dc === 'UBI1270'){
    $context['dc_id'] = 'X';
}elseif ($my_dc === 'UBI1654'){
    $context['dc_id'] = 'X';
}elseif ($my_dc === 'UBI1654'){
    $context['dc_id'] = 'Z';
}
$context['health']='active';
$response = prepare_json_response(ENDED, "order command execute successfull", $context, true);
echo $response;
?>
