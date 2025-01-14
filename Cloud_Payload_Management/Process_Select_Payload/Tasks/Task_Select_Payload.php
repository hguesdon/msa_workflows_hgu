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
 
  create_var_def('payload_descriptor', 'String');
 // create_var_def('service_order', 'String');
  create_var_def('e2e_service_order', 'String');
  create_var_def('vpn_service', 'String');
}

task_success('Payload Selected');
task_error('Task FAILED');
?>