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
$category=$context['source_type'];
//Update the e2e service with the ticket and its status}
$body=array();
if($category === 'DataCenter' || $category === 'DC'){
    $process_name="Process/workflows/E2E_Services_Management/Process_Update_DC_Ticket";
    $body['dc_tkt_id']=$context['tkt_id'];
    $body['dc_tkt_status']='closed';
    
}elseif($category === 'VPN'){
    $process_name="Process/workflows/E2E_Services_Management/Process_Update_VPN_Ticket";
    $body['vpn_tkt_id']=$context['tkt_id'];
    $body['vpn_tkt_status']='closed';
}else{
    task_success('E2E Service updated accordingly');
}

$json_body=json_encode($body);
$ubiqube_id=$context['UBIQUBEID'];
$serv_id=$context['e2e_service_order'];
$response =_orchestration_launch_process_instance ($ubiqube_id, $serv_id, $process_name, $json_body);
$response=json_decode($response,true);
if($response['wo_status'] !=='ENDED'){
  $response=json_encode($response);
  task_error($response);
}

task_success('E2E Service updated accordingly');
task_error('Task FAILED');
?>