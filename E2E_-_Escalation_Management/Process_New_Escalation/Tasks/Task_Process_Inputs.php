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
  create_var_def('source_id', 'String');
  create_var_def('e2e_service_order', 'String');
  create_var_def('source_type', 'String');
  create_var_def('alarm_details', 'String');
}

//Create a trouble ticket with source_type as category, alarm_details as description
$context['tkt_id']='';
$dev='UBIA1664';
$dev=getIdFromUbiId($dev);
$customerAccount='1183135126';
$description=$context['alarm_details'];
$severity='Urgent';
$category=$context['source_type'];
$creator='anhyper_comware_admin';
$source_id=$context['source_id'];;
$time_stamp=date("yy-m-d h:m:s");;


$obj_params=array();
$obj_params['customerAccount']=$customerAccount;
$obj_params['description']=$description;
$obj_params['severity']=$severity;
$obj_params['category']=$category;
$obj_params['creator']=$creator;
$obj_params['source_id']=$source_id;
$obj_params['time_stamp']=$time_stamp;

$cmd_obj=array("All_Tickets" => array("" => $obj_params));
$response = execute_command_and_verify_response($dev, CMD_CREATE, $cmd_obj, "Ticket Create");
$response=json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
    $response = json_encode($response);
    echo $response;
    exit;
}
sleep(10);
//import to fetch the tkt id
$tkt_id='';
$ms='All_Tickets';
while(true){
  $res=import_objects($dev,array($ms));
  $res=json_decode($res,true);
  if ($res['wo_status'] !== ENDED) {
    logToFile("Waiting for the ticket to be created");
    sleep(5);
  }else{
    $tkt_list=$res['wo_newparams']['All_Tickets'];
    foreach($tkt_list as $key => $val){
      if($val['description'] === $description){
        logToFile("ohoo my ticket is:  $key");
        $tkt_id=$key;
        break;
      }
    }
    break;
  }
}

if(!empty($tkt_id)){
  $context['tkt_id']=$tkt_id;
}
/*
//Update the e2e service with the ticket and its status}
$body=array();
if($category === 'DataCenter' || $category === 'DC'){
    $process_name="Process/workflows/E2E_Services_Management/Process_Update_DC_Ticket";
    $body['dc_tkt_id']=$context['tkt_id'];
    $body['dc_tkt_status']='open';
    
}else{
    $process_name="Process/workflows/E2E_Services_Management/Process_Update_VPN_Ticket";
    $body['vpn_tkt_id']=$context['tkt_id'];
    $body['vpn_tkt_status']='open';
}

$json_body=json_encode($body);
$ubiqube_id=$context['UBIQUBEID'];
$serv_id=$context['e2e_service_order'];
$response =_orchestration_launch_process_instance ($ubiqube_id, $serv_id, $process_name, $json_body);
$response=json_decode($response,true);
if($response['wo_status'] !=='ENDED'){
  $response=json_encode($response);
  task_error($response);
}
*/
/**
 * End of the task (choose one)
 */
task_success("Escalation created with tkt id: $tkt_id");
task_error('Task FAILED');
?>