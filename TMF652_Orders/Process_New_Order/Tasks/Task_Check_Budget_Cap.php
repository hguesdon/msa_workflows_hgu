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
$orderItem=$context['orderItem'];
$sensor=$orderItem[0]['resources'][0]['sensor'];

if($sensor === '192.168.100.75'){
    $serviceIdentifier='123';
}elseif($sensor === '192.168.100.55'){
    $serviceIdentifier='1231';
}else{
    $ret = prepare_json_response(ENDED, "Budget Cap Check is skipped", $context, true);
    echo "$ret\n";
}

$url='https://732vrtowk7.execute-api.eu-central-1.amazonaws.com/Prod/checkBudgetCap';
$HTTP_M = "POST";
$body = array(
   "serviceIdentifier" =>"$serviceIdentifier",
);
$body = json_encode($body);
$CURL_CMD="/usr/bin/curl";
$curl_cmd = "{$CURL_CMD} -isw '\nHTTP_CODE=%{http_code}' --connect-timeout 60 --max-time 60 -H \"Content-Type: application/json;charset=utf-8\" -X {$HTTP_M} -k '{$url}' -d '{$body}'";
logToFile("Naveen-$curl_cmd");
$response = perform_curl_operation($curl_cmd, "Calling POST HTTP method");

$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
  $response = json_encode($response);
  return $response;
exit;
}
$response=$response['wo_newparams']['response_body'];
$response = json_decode($response, true);
$resp=$response['budgetAvailable'];

$bill_id=$response['billingAccountId'];
logToFile("navi-$resp");
if($resp){
    $ret = prepare_json_response(ENDED, "Budget Available for Billing Account: $bill_id", $context, true);
    echo "$ret\n";
}else{
    $ret = prepare_json_response(FAILED, "Budget Cap reached for Billing Account: $bill_id", $context, true);
    echo "$ret\n";
}

?>