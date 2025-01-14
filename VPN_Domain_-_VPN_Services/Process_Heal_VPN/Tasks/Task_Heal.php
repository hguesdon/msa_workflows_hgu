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

//Read the Latency mapping for the remote_end_point(remote site line id) from the access infra resources
$ubi_id=$context['UBIQUBEID'];
$remote_end_point = $context['remote_end_point'];
$matching_resource='';

$response=_orchestration_list_service_instances ($ubi_id);
$response=json_decode($response,true);
if($response['wo_status'] !== 'ENDED'){
  logTofile("Could not list the WF instances");
}
$wf_list=$response['wo_newparams'];
$available_resource='';

foreach($wf_list as $wf){
  $service_id=$wf['id'];
  logToFile("Reading id: $service_id");
  if($wf['name'] === 'Process/Access_Infra_Resources/Access_Infra_Resources' && $wf['state'] === 'ACTIVE'){
    logToFile("Matching Reading id: $service_id");
    $resp=_orchestration_get_service_variables_by_service_id ($service_id);
    $resp=json_decode($resp,true);
    //logToFile(debug_dump($resp,"**************Response**********\n"));
    $item=$resp['wo_newparams'];
    foreach($item as $key => $val){
      if($val['name'] === 'line_id' && $val['value'] === $remote_end_point){
        $matching_resource=$service_id;
        foreach($item as $k =>$v){
          if($v['name'] === 'latency'){
            $context['total_latency']=$v['value'];
            break;
          }
        }
        break;
      }
    }
  }
  if($service_id === $matching_resource ){
    logToFile("Found matching access resource: $matching_resource");
    break;
  }
}

$context['health']='active';
$esc_sid=$context['escalation_sid'];
if(isset($esc_sid) && !empty($esc_sid)){
    //Close the escalation_sid
    $process_name="Process/workflows/E2E_-_Escalation_Management/Process_Notify_Reporter";
	$body=array();
	$body['resolution']="The VPN is now active";
	$json_body=json_encode($body);
	$ubiqube_id=$context['UBIQUBEID'];
	$response =_orchestration_launch_process_instance ($ubiqube_id, $esc_sid, $process_name, $json_body);
	$response=json_decode($response,true);
	if($response['wo_status'] !=='ENDED'){
	  $response=json_encode($response);
	  task_error($response);
	}
    //update the vpn tkt status in e2e service
    $context['vpn_tkt_status']='closed';
    
}
task_success('VPN Service Healed');
?>