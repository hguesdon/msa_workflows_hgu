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
$TOKEN='';
$id=$context['ticket_id'];
$full_url  = "https://your-infonova-api.com/r6-api/yourtenant/troubleTicketing/v1/tickets/$id";

$cat=$context['category'];
$body=array();

$body['state']='Closed"';

$head='Authorization: Bearer '.$TOKEN;
$HTTP_M = "PATCH";

$body = json_encode($body);
$CURL_CMD="/usr/bin/curl";
$curl_cmd = "{$CURL_CMD} -isw '\nHTTP_CODE=%{http_code}' --connect-timeout 60 --max-time 60 -H \"Content-Type: application/json\" -H '{$head}'  -X {$HTTP_M} -k '{$full_url}' -d '{$body}'";
$response = perform_curl_operation($curl_cmd, "Calling GET HTTP method");
$response = json_decode($response, true);

if ($response['wo_status'] !== ENDED) {
  $response = json_encode($response);
  return $response;
exit;
}

$r_data = json_decode($response["wo_newparams"]["response_body"]);
logToFile(debug_dump($r_data,"**************CURL CMD**********\n"));

task_success('Task OK');
?>