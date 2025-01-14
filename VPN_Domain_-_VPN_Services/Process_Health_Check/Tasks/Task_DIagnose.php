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


if ($context['health'] !== 'active') {
    //New Escalation which will Raise a trouble ticket and store the escalation SID
    //$context['escalation_sid']='';
    //$context['vpn_tkt_id']='';
    $source_id=$context['service_id'];
	$e2e_service_order=$context['e2e_service_order'];
	$source_type='VPN';
	$alarm_details="VPN Service-$source_id is not active";

	$service_name="Process/workflows/E2E_-_Escalation_Management/E2E_-_Escalation_Management";
	$process_name="Process/workflows/E2E_-_Escalation_Management/Process_New_Escalation";
	$body=array();
	$body['source_id']=$source_id;
	$body['e2e_service_order']=$e2e_service_order;
	$body['source_type']=$source_type;
	$body['alarm_details']=$alarm_details;
	$json_body=json_encode($body);
	$ubiqube_id=$context['UBIQUBEID'];
	$response =_orchestration_execute_service ($ubiqube_id, $service_name, $process_name, $json_body);
	$response=json_decode($response,true);
	if($response['wo_status'] !=='ENDED'){
	  $response=json_encode($response);
	  task_error($response);
	}
	logToFile(debug_dump($response,"**************Response**********\n"));
	$escalation_sid=$response['wo_newparams']['serviceId']['id'];
	$context['escalation_sid'] = $escalation_sid;

	$resp=_orchestration_get_service_variables_by_service_id ($escalation_sid);
	$resp=json_decode($resp,true);
	$item=$resp['wo_newparams'];
	foreach($item as $key => $val){
	    if($val['name'] === 'tkt_id') {
		$vpn_tkt_id=$val['value'];
		break;
	    }
	}
	if(isset($vpn_tkt_id) && !empty($vpn_tkt_id)){
	    $context['vpn_tkt_id']=$vpn_tkt_id;
	}
    $context['vpn_tkt_status']='open';
	$ret = prepare_json_response(WARNING, 'VPN is not active', $context, true);
	echo "$ret\n";
	exit;
}

//Read the Latency mapping for the remote_end_point(remote site line id) from the access infra resources
$ubi_id=$context['UBIQUBEID'];
$remote_end_point = $context['remote_end_point'];
$matching_resource='';
//Find a free Access infra resource
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


/**
 * End of the task (choose one)
 */
task_success('VPN Service Healthy');
?>