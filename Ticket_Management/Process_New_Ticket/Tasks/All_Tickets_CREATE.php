<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args()
{
  create_var_def('device_id', 'Device');
create_var_def('customerAccount', 'String');
create_var_def('severity', 'String');
create_var_def('category', 'String');
create_var_def('description', 'String');
create_var_def('creator', 'String');
create_var_def('source_id', 'String');

}

check_mandatory_param('device_id');

$device_id = $context['device_id'];
$prefix = substr($device_id, 0, 3);
$device_id = str_replace($prefix, '', $device_id);

$cat=$context['category'];
$body=array();
$body['customerAccount']=$context['customerAccount'];
$body['description']=$context['descripton'];
$body['severity']='Important';
$body['category']=$cat;
$body['creator']=$context['creator'];
$body['source_id']=$context['source'];
$body['time_stamp']=date("yy-m-d h:m:s");

$object_parameters=array("All_Tickets" => array("" => $body));

$response = execute_command_and_verify_response($device_id, "CREATE", $object_parameters, "CREATE All_Tickets");
  $response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = prepare_json_response($response['wo_status'], $response['wo_comment'], $context, true);
	echo $response;
	exit;
}
$my_id="0";
$ms='All_Tickets';
$res=import_objects($device_id,array($ms));
$res=json_decode($res,true);
if ($res['wo_status'] !== ENDED) {
 //failed
 $response = prepare_json_response(FAILED, "Could not import !!!", $response['wo_newparams'], true);
 echo $response;
}else{
   $tickets=$res['wo_newparams']['All_Tickets'];
   foreach($tickets as $key => $val){
      $value=$val['description'];
      $ref=$context['description'];
      if($value === $ref){
         logToFile("ohoo my ticket id is:  $key");
         $my_id=$key;
         break;
      }
   }
}

$context['ticket_id']=$my_id;

$response = prepare_json_response(ENDED, "Ticket create successfully: $my_id", $response['wo_newparams'], true);
echo $response;
?>
