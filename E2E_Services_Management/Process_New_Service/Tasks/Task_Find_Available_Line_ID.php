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
$line_id='';
$ubi_id = $context['UBIQUBEID'];
//Find a free Access infra resource
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
        if($val['name'] === 'status' && $val['value'] === 'free'){
          $available_resource=$service_id;
          foreach($item as $k =>$v){
            if($v['name'] === 'vlan'){
              $context['vlan']=$v['value'];
              break;
            }
          }
          foreach($item as $k =>$v){
            if($v['name'] === 'line_id'){
              $line_id=$v['value'];
              break;
            }
          }
          break;
        }
      }
    }
    if($service_id === $available_resource ){
      logToFile("Found free access resource: $available_resource");
      //$context['available_resource']=$available_resource;
      break;
    }
}

if(empty($available_resource)){
    task_error('No Access infra resource available');
}
$context['routes'][0]['line_id']=$line_id;
task_success('Task OK');
task_error('Task FAILED');
?>