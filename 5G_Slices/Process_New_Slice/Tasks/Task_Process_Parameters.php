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
  create_var_def('priority', 'Integer');
  create_var_def('sST', 'Integer');
  create_var_def('availability', 'String');
  create_var_def('dLLatency', 'String');
  create_var_def('uLLatency', 'String');
  create_var_def('dLThptPerUE', 'String');
  create_var_def('uLThptPerUE', 'String');
  create_var_def('coverageArea', 'String');
  create_var_def('maxNumberofUEs', 'Integer');
  create_var_def('status', 'String');
  create_var_def('access_location', 'String');
  create_var_def('billingAccount', 'String');
  create_var_def('externalId', 'String');
  create_var_def('serviceOrderId', 'String');
  }


task_success('Service Order parameters processed');
task_error('Task FAILED');
?>
