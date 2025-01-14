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

$process_name="Process/workflows/IPOP_2023/Process_Switch_to_1G_for_8209";
$sid='5381';
$ubiqube_id=$context['UBIQUBEID'];
$response =_orchestration_launch_process_instance ($ubiqube_id, $sid, $process_name, '{}');
$response=json_decode($response,true);
if($response['wo_status'] !=='ENDED'){
    $response=json_encode($response);
    task_error($response);
}
/**
 * End of the task (choose one)
 */
task_success('Switch_to_1G_for_8209 process is triggerred');
task_error('Task FAILED');
?>