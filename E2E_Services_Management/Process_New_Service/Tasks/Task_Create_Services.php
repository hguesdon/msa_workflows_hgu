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
$dc_id='';
$dc_dev='';
$ubiqube_id=$context['UBIQUBEID'];
$components=$context['components'];
foreach ($components as $item){
    $type=$item['service_type'];
    if($type === 'DataCenter' || $type === 'DC'){
        $dc_id=$item['resource_id'];
        break;
    }
}
if(!empty($dc_id)){
    if($dc_id === 'X' || $dc_id === 'x'){
        $dc_dev='UBI1270';
    }elseif($dc_id === 'Y' || $dc_id === 'y'){
        $dc_dev='UBI1654';
    }else{
        task_error("Task FAILED: DC id $dc_id not found");
    }
} else{
    task_error("Task FAILED: DC id not specified in the service components");
}
$i=0;
$vpn_service_id='';
 foreach ($components as $item){
    $type=$item['service_type'];
    if($type === 'DataCenter' || $type === 'DC'){
        //Create DC payload deployment Service instance
        $service_name="Process/workflows/Cloud_Payload_Management/Cloud_Payload_Management";
        $process_name="Process/workflows/Cloud_Payload_Management/Process_Select_Payload";
        $body=array();
        $body['e2e_service_order']=$context['service_id'];
        $body['payload_descriptor']='Smart_Turtle_Bot';
        $body['vpn_service']=$vpn_service_id;
        $body['k8_device_id']=$dc_dev;
        $json_body=json_encode($body);
        
        $response =_orchestration_execute_service ($ubiqube_id, $service_name, $process_name, $json_body);
        $response=json_decode($response,true);
        if($response['wo_status'] !=='ENDED'){
            $response=json_encode($response);
            task_error($response);
        }
        logToFile(debug_dump($response,"**************Response**********\n"));
        $sid=$response['wo_newparams']['serviceId']['id'];
        //$context['service_order']=$sid;
        $context['components'][$i]['service']=$sid;
    }else if($type === 'VPN'){
        //Create VPN Service instance
        $service_name="Process/workflows/VPN_Domain_-_VPN_Services/VPN_Domain_-_VPN_Services";
        $process_name="Process/workflows/VPN_Domain_-_VPN_Services/Process_New_VPN";
        $body=array();
        $body['e2e_service_order']=$context['service_id'];
        $body['remote_end_point']=$context['routes'][0]['line_id'];
        $body['dc_end_point']=$dc_dev;
        $json_body=json_encode($body);
        $ubiqube_id=$context['UBIQUBEID'];
        $response =_orchestration_execute_service ($ubiqube_id, $service_name, $process_name, $json_body);
        $response=json_decode($response,true);
        if($response['wo_status'] !=='ENDED'){
            $response=json_encode($response);
            task_error($response);
        }
        logToFile(debug_dump($response,"**************Response**********\n"));
        $vpn_service_id=$response['wo_newparams']['serviceId']['id'];
        //$context['service_order']=$vpn_service_id;
        $context['components'][$i]['service']=$vpn_service_id;
        $context['components'][$i]['resource_id']=$context['routes'][0]['line_id'];
    }
    $i++;
}
$context['dc_dev']=$dc_dev;


task_success('Task OK');
task_error('Task FAILED');
?>