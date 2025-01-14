<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args()
{
  //create_var_def('device_id', 'Device');
  
}


$device_id = 'POP1914';
$prefix = substr($device_id, 0, 3);
$device_id = str_replace($prefix, '', $device_id);

$object_parameters['ONUs'] = '0';


$response = execute_command_and_verify_response($device_id, "IMPORT", $object_parameters, "IMPORT ONUs");
  $response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = prepare_json_response($response['wo_status'], $response['wo_comment'], $context, true);
	echo $response;
	exit;
}
$context['current_count']=sizeof($response['wo_newparams']['ONUs']);
$cur_count=$context['current_count'];
if(isset($context['last_count']))
	$last_count=$context['last_count'];
else
	$last_count=6;

logToFile("the number of MS is: $cur_count");
if($cur_count > $last_count){
	$msg = 'Condition deteted to trigger the 10G provisioning';
	//Trigger the "Provision 10G for ONUs" WF process of "IPOP 2023" WF
    $process_name="Process/workflows/IPOP_2023/Process_Provision_10G_for_ONUs";
    $sid='5381';
    $ubiqube_id=$context['UBIQUBEID'];
    $response =_orchestration_launch_process_instance ($ubiqube_id, $sid, $process_name, '{}');
    $response=json_decode($response,true);
    if($response['wo_status'] !=='ENDED'){
        $response=json_encode($response);
        task_error($response);
    }
}
else {
	$msg = 'No change in NUmber of ONUs deteted';
}
$context['last_count'] = $context['current_count'];
$response = prepare_json_response(ENDED, "$msg", $context, true);
echo $response;
?>
