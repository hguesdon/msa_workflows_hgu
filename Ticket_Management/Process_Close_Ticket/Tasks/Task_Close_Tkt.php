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
$id=$context['ticket_id'];
$object_parameters=array("All_Tickets" => array("$id" => array()));

$response = execute_command_and_verify_response($device_id, "UPDATE", $object_parameters, "Close Ticket");
  $response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = prepare_json_response($response['wo_status'], $response['wo_comment'], $context, true);
	echo $response;
	exit;
}

task_success('Ticket closed!');
task_error('Task FAILED');
?>