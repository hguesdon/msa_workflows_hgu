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
$sid=$context['available_access_resource'];
$process_name='Process/Access_Infra_Resources/Free';
$ubiqube_id=$context['UBIQUBEID'];
_orchestration_launch_process_instance ($ubiqube_id, $sid, $process_name, $json_body = "{}");
task_success('Task OK');
task_error('Task FAILED');
?>