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
 
  create_var_def('dc_tkt_status', 'String');
}
$dc_tkt_status=$context['dc_tkt_status'];
$esc_sid=$context['escalation_sid'];
logToFile("Tamtam: $esc_sid");
//Close escalation
$process_name="Process/workflows/E2E_-_Escalation_Management/Process_Notify_Reporter";
$body=array();
$body['resolution']=$dc_tkt_status;
$json_body=json_encode($body);
$ubiqube_id=$context['UBIQUBEID'];
$response =_orchestration_launch_process_instance ($ubiqube_id, $esc_sid, $process_name, $json_body);
$response=json_decode($response,true);
if($response['wo_status'] !=='ENDED'){
  $response=json_encode($response);
  task_error($response);
}
//update the vpn tkt status in e2e service
$context['dc_tkt_status']="closed: $dc_tkt_status";

$context['escalation_sid'] = '';
$context['health']='active';
task_success('Task OK');
task_error('Task FAILED');
?>