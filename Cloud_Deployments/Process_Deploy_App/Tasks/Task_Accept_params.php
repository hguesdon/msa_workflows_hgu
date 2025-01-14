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
  /**
   * You can use var_name convention for your variables
   * They will display automaticaly as "Var Name"
   * The allowed types are:
   *    'String', 'Boolean', 'Integer', 'Password', 'IpAddress',
   *    'IpMask', 'Ipv6Address', 'Composite', 'OBMFRef', 'Device'
   *
   * Add as many variables as needed
   */
  create_var_def('environment', 'String');
  create_var_def('app_repo', 'String');
  create_var_def('app', 'String');
  create_var_def('app_ver', 'String');
  create_var_def('callback_wf', 'String');
  create_var_def('callback_process', 'String');
  create_var_def('callback_params.0.name', 'String');
  create_var_def('callback_params.0.value', 'String');
  create_var_def('pipeline_id', 'String');
}


/**
 * End of the task (choose one)
 */
task_success('Task OK');
task_error('Task FAILED');
?>