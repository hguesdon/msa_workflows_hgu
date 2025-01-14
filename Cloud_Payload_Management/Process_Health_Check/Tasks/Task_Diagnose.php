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
$status=$context['health'];
if($status !== 'active'){
    //Escalate and get the escalation sid which will raise a DC ticket
    //$context['escalation_sid']='';
    //$context['dc_tkt_id']='';
    $source_id=$context['service_id'];
	$e2e_service_order=$context['e2e_service_order'];
	$source_type='DataCenter';
	$alarm_details="DC Service-$source_id is $status";

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
    sleep(5);
	$resp=_orchestration_get_service_variables_by_service_id ($escalation_sid);
	$resp=json_decode($resp,true);
	$item=$resp['wo_newparams'];
	foreach($item as $key => $val){
	    if($val['name'] === 'tkt_id') {
		$dc_tkt_id=$val['value'];
		break;
	    }
	}
	if(isset($dc_tkt_id) && !empty($dc_tkt_id)){
	    $context['dc_tkt_id']=$dc_tkt_id;
	}
    $context['dc_tkt_status']='open';
    task_error('DC is not active');
    exit;

}
//if vpn is not healthy, create a related DC escalation and end with warning
//Read the VPN service health and not the health check process
//The DC health will remain active irrespective of the VPN issue
$vpn_serv_id=$context['vpn_service'];
$vpn_health='';
sleep(5);
$resp=_orchestration_get_service_variables_by_service_id ($vpn_serv_id);
$resp=json_decode($resp,true);
//logToFile(debug_dump($resp,"**************Response**********\n"));
$item=$resp['wo_newparams'];
foreach($item as $key => $val){
    if($val['name'] === 'health') {
        $vpn_health=$val['value'];
        break;
    }
}
if(!empty($vpn_health) && $vpn_health !== 'active'){
    //Raise a DC Escalation on the VPN issue at the moment
    $source_id=$context['service_id'];
	$e2e_service_order=$context['e2e_service_order'];
	$source_type='DataCenter';
	$alarm_details="DC Service-$source_id is interrupted for unkknow reason";

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
		$dc_tkt_id=$val['value'];
		break;
	    }
	}
	if(isset($dc_tkt_id) && !empty($dc_tkt_id)){
	    $context['dc_tkt_id']=$dc_tkt_id;
	}else{
	    sleep(10);
	    $resp=_orchestration_get_service_variables_by_service_id ($escalation_sid);
	    $resp=json_decode($resp,true);
	    $item=$resp['wo_newparams'];
	    foreach($item as $key => $val){
	        if($val['name'] === 'tkt_id') {
	            $dc_tkt_id=$val['value'];
	            break;
	            }
	    }
	    if(isset($dc_tkt_id) && !empty($dc_tkt_id)){
	        $context['dc_tkt_id']=$dc_tkt_id;
	       /* }else{
	            task_error("Issue while fetching ticket details from escalation");*/
	        }
	}
    $context['dc_tkt_status']='open';
    $response = prepare_json_response(WARNING, "DC Service is impacted by an issue of VPN", $context, true);
    echo $response;
}
    
task_success('DC is all healthy');

?>