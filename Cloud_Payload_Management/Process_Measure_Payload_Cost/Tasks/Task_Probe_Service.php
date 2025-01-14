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
$alternate_DC='UBI1270';
$y=$context['k8_device_id'];
if($alternate_DC === $y){
    $alternate_DC='UBI1654';
}
$context['best_node']=$y;
$dev=getIdFromUbiId($y);
//Identify the usage of altrernate DC options and if any found better, set that as the new destination
$resp=_configuration_variable_read($dev,'USAGE');
logToFile("blo:$resp\n");
$resp=json_decode($resp,true);
$cur_usage=$resp['wo_newparams']['value'];

$dev=getIdFromUbiId($alternate_DC);
$resp=_configuration_variable_read($dev,'USAGE');
logToFile("blo:$resp\n");
$resp=json_decode($resp,true);
$alt_usage=$resp['wo_newparams']['value'];
//If any single option is same as the current DC then choose the best latency DC
if($cur_usage > $alt_usage){
    //we have to choose the alternate DC
    $context['best_node']=$alternate_DC;
}else if($cur_usage === $alt_usage){
    //Choose the smallest latency DC
    $dev=getIdFromUbiId($y);
    $resp=_configuration_variable_read($dev,'LATENCY');
    logToFile("lolo:$resp\n");
    $resp=json_decode($resp,true);
    $cur_latency=$resp['wo_newparams']['value'];
    
    $dev=getIdFromUbiId($alternate_DC);
    $resp=_configuration_variable_read($dev,'LATENCY');
    logToFile("lolo:$resp\n");
    $resp=json_decode($resp,true);
    $alt_latency=$resp['wo_newparams']['value'];
    if($cur_latency > $alt_latency){
        //we have to choose the alternate DC
        $context['best_node']=$alternate_DC;
    }
}

$context['new_destination']=$context['best_node'];

$x=$context['new_destination'];


if($x===$y){
    $response = prepare_json_response(WARNING, "Current node is already optimal", $context, true);
    echo $response;
}
task_success('New Destination node selected');
?>