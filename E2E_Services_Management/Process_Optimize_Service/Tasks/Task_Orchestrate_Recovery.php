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


$dc_end_point=$context['new_DC_dev_id'];
$remote_end_point='';
$e2e_service_order=$context['service_id'];
$vpn_service_id = '';
$old_vpn='';
$components = $context['components'];
//Provision new VPN service with new DC end point
$i=0;
foreach ($components as $item){
    $type=$item['service_type'];
    if($type === 'VPN'){
        //get Old VPN service id to delete it later
        $old_vpn=$item['service'];
        //Create VPN Service instance
        $service_name="Process/workflows/VPN_Domain_-_VPN_Services/VPN_Domain_-_VPN_Services";
        $process_name="Process/workflows/VPN_Domain_-_VPN_Services/Process_New_VPN";
        $body=array();
        $body['e2e_service_order']=$context['service_id'];
        $body['remote_end_point']=$context['routes'][0]['line_id'];
        $body['dc_end_point']=$dc_end_point;
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
        break;
    }
    $i++;
}

//Update the VPN Service in DC - cloud payload mgmt
//Confirm the updating of DC service with optimal DC resource
$ubiqube_id=$context['UBIQUBEID'];
$components = $context['components'];
$i=0;
foreach ($components as $item){
    $type=$item['service_type'];
    if($type === 'DataCenter' || $type === 'DC'){
        //Find optimal DC resource in the DC service
        $sid=$item['service'];
        $process_name="Process/workflows/Cloud_Payload_Management/Process_Migrate_Payload";
        
        $json_body='{}';
        $response =_orchestration_launch_process_instance ($ubiqube_id, $sid, $process_name, $json_body);
        $response=json_decode($response,true);
        if($response['wo_status'] !=='ENDED'){
            $response=json_encode($response);
            task_error($response);
        }
        
        //Update the DC service with the new VPN service
        $process_name="Process/workflows/Cloud_Payload_Management/Process_Update_VPN";
        $body=array();
        $body['vpn_service'] = $vpn_service_id;
        $json_body=json_encode($body);
        $response =_orchestration_launch_process_instance ($ubiqube_id, $sid, $process_name, $json_body);
        $context['components'][$i]['resource_id']=$context['new_dc_id'];
        break;
    }
    $i++;
}

//Decommission old VPN resource
$process_name="Process/workflows/VPN_Domain_-_VPN_Services/Process_Decommission_VPN";

$json_body='{}';
$ubiqube_id=$context['UBIQUBEID'];
$response =_orchestration_launch_process_instance ($ubiqube_id, $old_vpn, $process_name, $json_body);


task_success('Task OK');
task_error('Task FAILED');
?>