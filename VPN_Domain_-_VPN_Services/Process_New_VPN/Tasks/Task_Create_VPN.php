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
  //create_var_def('service_order', 'String');
  create_var_def('e2e_service_order', 'String');
  create_var_def('remote_end_point', 'String');
  create_var_def('dc_end_point', 'String');
  
}
//Read the Latency mapping for the remote_end_point(remote site line id) from the dedicated table
$ubi_id=$context['UBIQUBEID'];
$remote_end_point = $context['remote_end_point'];
$matching_resource='';
//Read the Access infra resources to fetch the latency
$response=_orchestration_list_service_instances ($ubi_id);
$response=json_decode($response,true);
if($response['wo_status'] !== 'ENDED'){
  logTofile("Could not list the WF instances");
}
$wf_list=$response['wo_newparams'];
$available_resource='';

foreach($wf_list as $wf){
  $service_id=$wf['id'];
  logToFile("Reading id: $service_id");
  if($wf['name'] === 'Process/Access_Infra_Resources/Access_Infra_Resources' && $wf['state'] === 'ACTIVE'){
    logToFile("Matching Reading id: $service_id");
    $resp=_orchestration_get_service_variables_by_service_id ($service_id);
    $resp=json_decode($resp,true);
    //logToFile(debug_dump($resp,"**************Response**********\n"));
    $item=$resp['wo_newparams'];
    foreach($item as $key => $val){
      if($val['name'] === 'line_id' && $val['value'] === $remote_end_point){
        $matching_resource=$service_id;
        foreach($item as $k =>$v){
          if($v['name'] === 'latency'){
            $context['total_latency']=$v['value'];
            break;
          }
        }
        break;
      }
    }
  }
  if($service_id === $matching_resource ){
    logToFile("Found matching access resource: $matching_resource");
    $available_resource = $matching_resource;
    break;
  }
}
if(empty($available_resource)){
    task_error('Task FAILED: Could not find available access resource- Remote Line ID');
}
//Update the access infra resource to allocate
$process_name='Process/Access_Infra_Resources/Allocate';
$body=array();
$body['sub_order']=$context['service_id'];
$body['service_order']=$context['e2e_service_order'];
$body['port']='FastEthernet0/10';
$json_body=json_encode($body);
_orchestration_launch_process_instance ($ubi_id, $available_resource, $process_name, $json_body);


$process_name='Process/Access_Infra_Resources/Confirm_Allocation';
_orchestration_launch_process_instance ($ubi_id, $available_resource, $process_name, $json_body = "{}");

$context['available_access_resource']=$available_resource;
//update the status to active
$context['health']='active';

task_success('VPN Service Created');
task_error('Task FAILED');
?>