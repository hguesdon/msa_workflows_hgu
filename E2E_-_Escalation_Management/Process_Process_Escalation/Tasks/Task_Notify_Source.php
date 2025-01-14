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
$source_type=$context['source_type'];
$process_name="Process/workflows/Cloud_Payload_Management/Process_Update_RC";
if($source_type ==='DataCenter'){
    $sid=$context['source_id'];
    $body=array();
    $body['dc_tkt_status']=$context['resolution'];
}elseif($source_type === 'Service'){
    $sid=$context['service_id'];
    //Close the E2E escalation first and then Notify the DC payload mgmt service to close the DC ticket
    $process_name="Process/workflows/E2E_-_Escalation_Management/Process_Notify_Reporter";
    $body=array();
    $body['resolution']=$context['resolution'];
    $json_body=json_encode($body);
    $ubiqube_id=$context['UBIQUBEID'];
    $response =_orchestration_launch_process_instance ($ubiqube_id, $sid, $process_name, $json_body);
    $response=json_decode($response,true);
    if($response['wo_status'] !=='ENDED'){
        $response=json_encode($response);
        task_error($response);
    }
    //Now Notify the RC to the DC cloud service which will close the DC ticket as well
    $sid=$context['service_DC_source'];
    $process_name="Process/workflows/Cloud_Payload_Management/Process_Update_RC";
    $body=array();
    $body['dc_tkt_status']=$context['dc_resolution'];
    
}
sleep(5);
$json_body=json_encode($body);
$ubiqube_id=$context['UBIQUBEID'];
$response =_orchestration_launch_process_instance ($ubiqube_id, $sid, $process_name, $json_body);
$response=json_decode($response,true);
if($response['wo_status'] !=='ENDED'){
  $response=json_encode($response);
  task_error($response);
}

task_success('Root cause updated to the Source of the Escalation');
task_error('Task FAILED');
?>