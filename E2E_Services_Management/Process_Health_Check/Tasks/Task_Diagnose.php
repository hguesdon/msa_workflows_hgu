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

//If the overall service is up and optimal the task will run successfully
//In case the status is up but not optimal, the task will update the optimal route and ends with warning
//Incase the status is not up, then the task will fail
$sub_services=$context['components'];
$status='active';
foreach($sub_services as $component ){
    $sid=$component['service'];
    $sid_type=$component['service_type'];
    //Read the service health variable from the sid
    $sid_health='';
    logToFile("mow: $sid");
    if($sid_type === 'DataCenter' || $sid_type === 'DC'){
        $resp=_orchestration_get_service_variables_by_service_id ($sid);
        $resp=json_decode($resp,true);
        $item=$resp['wo_newparams'];
        foreach($item as $key => $val){
            if($val['name'] === 'health') {
                $sid_health=$val['value'];
                logToFile("navnav: $sid_health");
                
            }
            
        }if(!empty($sid_health) && $sid_health !== 'active'){
            $status  = $sid_health;
        }
    }elseif($sid_type === 'VPN'){
        $resp=_orchestration_get_service_variables_by_service_id ($sid);
        $resp=json_decode($resp,true);
        $item=$resp['wo_newparams'];
        foreach($item as $key => $val){
            if($val['name'] === 'health') {
                $sid_health=$val['value'];
                logToFile("vnavnav: $sid_health");
                
            }
            
        }if(!empty($sid_health) && $sid_health !== 'active'){
            logToFile("kavav: $sid_health :::");
            $status  = 'failed';
        }
        logToFile("I am here!!");
    }
}

$context['status']=$status;
if($status !== 'active'){
    task_warning("E2E Service is not healthy");
}

task_success('Task OK');
task_error('Task FAILED');
?>