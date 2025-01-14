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

//$billingId=$context['billingAccount'];
//task_success("Slice decommissioned for the billing account: $billingId");
task_success("Slice decommissioned");
task_error('Task FAILED');
?>