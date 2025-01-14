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
//Identify the E2E Service/s that contains the source_id(domain specific service ID) of the escalation

task_success('E2E Service Identified');
task_error('Task FAILED');
?>