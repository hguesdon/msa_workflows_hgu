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
    create_var_def('resolution', 'String');
}
//If the Root cause exists for the given escalation, then notify the escalation source instance about the RC
$tt_id=$context['tkt_id'];
$resolution=$context['resolution'];
$dev='UBIA1664';
$dev=getIdFromUbiId($dev);

//Close the tt and update e2e_service with the tkt status for closed tkt 
//Create a trouble ticket with source_type as category, alarm_details as description
$tkt_id=$context['tkt_id'];
$obj_params=array();
$obj_params['description']=$resolution;
$object_params['object_id']=$tkt_id;

$cmd_obj=array("All_Tickets" => array("$tkt_id" => $obj_params));
$response = execute_command_and_verify_response($dev, CMD_UPDATE, $cmd_obj, "Ticket update");
$response=json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
    $response = json_encode($response);
    echo $response;
    exit;
}


task_success('Closed the escalation');
task_error('Task FAILED');
?>