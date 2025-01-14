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
/*$billingAccount=$context['relatedObjects'][0]['owner'];
$type=$context['orderItems'][0]['service']['name'];

if($type === '5G'){
    //Create DC payload deployment Service instance
    $service_name="Process/workflows/5G_Slices/5G_Slices";
    $process_name="Process/workflows/5G_Slices/Process_New_Slice";
    $body=array();
    $body['billingAccount']=$billingAccount;
    $body['priority']=4;
    $body['sST']=1;
    $body['availability']='99.999%';
    $body['dLLatency']='10ms';
    $body['uLLatency']='10ms';
    $body['dLThptPerUE']='100Mb';
    $body['uLThptPerUE']='100Mb';
    $body['coverageArea']='Stadium A';
    $body['maxNumberofUEs']=2;
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
    $context['provisioned_service']=$sid;
}
elseif($type === 'DEEPTECTOR_SERVICE'){
    	
} elseif($type === 'MEC'){
	
}
    */
task_success('Task OK');
task_error('Task FAILED');
?>