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
  create_var_def('alarmRaisedTime', 'String');
  create_var_def('alarmType', 'String');
  create_var_def('alarmedObject.0.sensor', 'String');
  create_var_def('alarmedObject.0.monitor', 'String');
  create_var_def('alarmedObject.0.farmer', 'String');
  create_var_def('perceivedSeverity', 'String');
  create_var_def('probableCause', 'String');
  create_var_def('sourceSystemId', 'String');
  create_var_def('state', 'String');
}



task_success('Input processed OK');
task_error('Task FAILED');
?>