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
$ubiqube_id=$context['UBIQUBEID'];
$components = $context['components'];
$new_DC_dev_id = '';
$new_dc_id='';
foreach ($components as $item){
    $type=$item['service_type'];
    if($type === 'DataCenter' || $type === 'DC'){
        //Find optimal DC resource in the DC service
        $sid=$item['service'];
        $process_name="Process/workflows/Cloud_Payload_Management/Process_Measure_Payload_Cost";

        $response =_orchestration_launch_process_instance ($ubiqube_id, $sid, $process_name, '{}');
        $response=json_decode($response,true);
        if($response['wo_status'] !=='ENDED'){
            $response=json_encode($response);
            task_error($response);
        }
        //Find the new DC resource id/endpoint for the VPN update and store
        //Thus id the need for change of VPN endpoint
        sleep(10);
        $resp=_orchestration_get_service_variables_by_service_id ($sid);
        $resp=json_decode($resp,true);
        $item=$resp['wo_newparams'];
        foreach($item as $key => $val){
            if($val['name'] === 'new_destination') {
                $new_DC_dev_id=$val['value'];
                break;
            }
        }
        if(!empty($new_DC_dev_id)){
            if($new_DC_dev_id === 'UBI1270' ){
                $new_dc_id='X';
            }elseif($new_DC_dev_id === 'UBI1654' ){
                $new_dc_id='Y';
            }else{
                task_error("Task FAILED: DC id $dc_id not found");
            }
        }
        break;
    }
}
$context['new_dc_id'] = $new_dc_id;
$context['new_DC_dev_id']=$new_DC_dev_id;


task_success('Task OK');
task_error('Task FAILED');
?>