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
  create_var_def('orderItem.0.action', 'String');
  create_var_def('orderItem.0.resources.0.sensor', 'String');
  create_var_def('orderItem.0.resources.0.name', 'String');
  create_var_def('orderItem.0.resources.0.monitor', 'String');
  create_var_def('orderItem.0.resources.0.farmer', 'String');
}


task_success('Task OK');
task_error('Task FAILED');
?>