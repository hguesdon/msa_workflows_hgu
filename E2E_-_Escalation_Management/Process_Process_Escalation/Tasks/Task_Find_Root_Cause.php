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
//If the e2e service  health is good in hte previous task, proceed to find the RC of the issue and capture it
//In our self healing example, VPN domain will raise a ticket and close it after autoremediation
//Hence capture the ticket if of the closed VPN ticket as a root cause
$e2e_service_order=$context['e2e_service_order'];
//Fetch the closed VPN ticket for the e2e service order
$resp=_orchestration_get_service_variables_by_service_id ($e2e_service_order);
$resp=json_decode($resp,true);
$item=$resp['wo_newparams'];
$source_type=$context['source_type'];
$vpn_tkt_id='';
if($source_type === 'DataCenter' || $source_type === 'DC'){
    foreach($item as $key => $val){
        if($val['name'] === 'vpn_tkt_id') {
            $vpn_tkt_id=$val['value'];
        }
        if($val['name'] === 'vpn_tkt_status') {
            $vpn_tkt_status=$val['value'];
        }
    }
    logToFile("VPN Ticket: $vpn_tkt_id ------Status: $vpn_tkt_status\n");
    $context['resolution']="Root Cause: $vpn_tkt_id in VPN Domain";
    task_success('Task OK');
}elseif($source_type === 'Service'){
    //Fetch the DC escalation id and then Notify the DC service in the next task
    $components=array();
    foreach($item as $key => $val){
        if($val['name'] === 'components') {
            $components=$val['value'];
            break;
        }
        
    }
    foreach($components as $serv){
        $type=$serv['service_type'];
        if($type === 'DataCenter'){
            $context['service_DC_source']=$serv['service'];
        }
    }
    $var=$context['service_DC_source'];
    logToFile("DC Escalation sid from e2e service: $var\n");
    $context['dc_resolution']="DC Service is now optimized";
    $context['resolution']="E2E Service now updated and optimized";
    task_success('Task OK');
}
task_error('Task FAILED');

?>