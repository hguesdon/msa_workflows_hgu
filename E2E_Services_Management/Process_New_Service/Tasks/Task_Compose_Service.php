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

  create_var_def('components.0.service', 'String');
  create_var_def('components.0.service_type', 'String');
  create_var_def('components.0.resource_id', 'String');
//  create_var_def('routes.0.line_id', 'String');
  create_var_def('status', 'Status');
}


task_success('Task OK');
?>