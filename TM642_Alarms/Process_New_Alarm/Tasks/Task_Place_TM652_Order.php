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
$service_name="Process/workflows/TMF652_Orders/TMF652_Orders";
$process_name="Process/workflows/TMF652_Orders/Process_New_Order";

$name=$context['sourceSystemId'];
$sensor=$context['alarmedObject'][0]['sensor'];
$monitor=$context['alarmedObject'][0]['monitor'];
$farmer=$context['alarmedObject'][0]['farmer'];
$action="add";
$ritem = array(
   "name" =>"$name",
   "sensor"=>"$sensor",
   "monitor" => "$monitor",
   "farmer" => "$farmer"
);
$resources=array();
array_push($resources,$ritem);
$r_obj=array(
	"action" => "$action",
	"resources" => $resources

);

$items=array();
array_push($items,$r_obj);
$body=array(
	"orderItem" => $items
);


$json_body=json_encode($body);
$ubiqube_id=$context['UBIQUBEID'];
$response =_orchestration_execute_service ($ubiqube_id, $service_name, $process_name, $json_body);
$response=json_decode($response,true);
if($response['wo_status'] !=='ENDED'){
  $response=json_encode($response);
  task_error($response);
}
//logToFile(debug_dump($response,"**************Response**********\n"));
$res_id=$response['wo_newparams']['serviceId']['id'];
$context['res_id']=$res_id;


//If resource set is not available
//Notify Resource Availability as negative
//task_error('No Resources available');

//Notify Resource Availability
task_success('Switch updated accordingly');

?>