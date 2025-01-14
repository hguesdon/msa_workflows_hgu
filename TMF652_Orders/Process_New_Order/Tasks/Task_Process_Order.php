<?php
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args()
{
}

$orderItem=$context['orderItem'];
$name=$orderItem[0]['resources'][0]['name'];
$sensor=$orderItem[0]['resources'][0]['sensor'];
$monitor=$orderItem[0]['resources'][0]['monitor'];
$farmer=$orderItem[0]['resources'][0]['farmer'];
$action=$orderItem[0]['action'];

$full_url  = "http://114.156.65.250:18080";
$HTTP_M = "POST";

//$est=date("yy-m-d");


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
	"resource" => $resources

);

$items=array();
array_push($items,$r_obj);
$body=array(
	"orderItem" => $items
);


//$head='corp: p1=TMFPOC01&cnt=1&d=42a9c684be4950b3b0d6c29645641e350457784ef7cfb4804ec31d9a2f4184a2';

$body = json_encode($body);
$CURL_CMD="/usr/bin/curl";
$curl_cmd = "{$CURL_CMD} -isw '\nHTTP_CODE=%{http_code}' --connect-timeout 60 --max-time 60 -H \"Content-Type: application/json;charset=utf-8\" -X {$HTTP_M} -k '{$full_url}' -d '{$body}'";
logToFile("Naveen-$curl_cmd");
$response = perform_curl_operation($curl_cmd, "Calling POST HTTP method");
$response = json_decode($response, true);

if ($response['wo_status'] !== ENDED) {
  $response = json_encode($response);
  return $response;
exit;
}

//$r_data = json0.0.0.0_decode($response["wo_newparams"]["response_body"]);
//logToFile(debug_dump($r_data,"**************CURL CMD**********\n"));

task_success('Order placed for IOWN Switch');
?>