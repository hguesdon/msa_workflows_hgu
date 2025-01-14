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

  create_var_def('externalId', 'String');
  create_var_def('priority', 'Integer');
  create_var_def('requestedStartDate', 'String');
  create_var_def('requestedCompletionDate', 'String');
  create_var_def('notificationContact', 'String');
  create_var_def('notes.0.date', 'String');
  create_var_def('notes.0.author', 'String');
  create_var_def('relatedParties.0.role', 'String');
  create_var_def('relatedParties.0.id', 'String');
  create_var_def('relatedParties.0.name', 'String');
  create_var_def('orderItems.0.id', 'String');
  create_var_def('orderItems.0.orderItemAction', 'String');
  create_var_def('orderItems.0.service.id', 'String');
  create_var_def('orderItems.0.service.name', 'String');
  create_var_def('orderItems.0.service.serviceIdentifier', 'String');
  create_var_def('orderItems.0.service.action', 'String');
  create_var_def('orderItems.0.service.serviceCharacteristics.0.id', 'String');
  create_var_def('orderItems.0.service.serviceCharacteristics.0.name', 'String');
  create_var_def('orderItems.0.service.serviceCharacteristics.0.type', 'String');
  create_var_def('orderItems.0.service.serviceCharacteristics.0.action', 'String');
  create_var_def('orderItems.0.service.serviceCharacteristics.0.value', 'String');
  create_var_def('relatedObjects.0.type', 'String');
  create_var_def('relatedObjects.0.id', 'String');
  create_var_def('relatedObjects.0.tenant', 'String');
  create_var_def('relatedObjects.0.distance', 'Integer');
  create_var_def('relatedObjects.0.orderType', 'String');
  create_var_def('relatedObjects.0.owner', 'String');
  create_var_def('relatedOrder.relationType', 'String');
  create_var_def('relatedOrder.id', 'String');
  
}

task_success('Task OK');
task_error('Task FAILED');
?>